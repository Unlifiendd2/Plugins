---
name: propale-doc-reviewer
description: >-
  Revue critique indépendante d'une trame de proposition commerciale selon trois axes simultanés.
  Lance 3 sous-agents spécialisés en parallèle (storytelling, cohérence, pertinence) — chacun
  écrit son analyse dans un fichier temporaire. Un 4ème agent de synthèse lit ces fichiers et
  produit le rapport final. L'orchestrateur ne touche jamais au contenu des fichiers.
  Phrases déclencheuses : « lance une revue complète », « audit multi-axes », « analyse ma propale »,
  « challenge cette trame », « revue indépendante », « passe la trame en revue ».
---

# Revue indépendante d'une trame de proposition commerciale

## Rôle et principe d'exécution

Ce skill orchestre une revue structurée en deux phases : **3 sous-agents spécialisés lancés en parallèle**, chacun couvrant un axe distinct, puis **1 agent de synthèse** qui lit leurs fichiers de résultats et produit le rapport final.

L'architecture garantit trois isolements stricts :
- Les 3 agents de revue travaillent chacun dans leur propre contexte frais, sans influence mutuelle.
- Chaque agent écrit son résultat dans un fichier temporaire dédié et ne retourne rien d'autre qu'une confirmation.
- L'agent de synthèse est le seul à lire les 3 fichiers et à croiser les analyses.

Ce skill est **autonome et non-interactif** : si une information manque, formuler une hypothèse et continuer.

## Règle fondamentale de l'orchestrateur

> **L'orchestrateur ne lit JAMAIS le contenu d'un fichier.**

Cette règle est absolue et sans exception :
- Il ne lit pas la trame à analyser.
- Il ne lit pas les fichiers temporaires produits par les agents de revue.
- Il ne lit pas le fichier final produit par l'agent de synthèse.
- Il ne traite que des **chemins de fichiers** : il les reçoit en entrée, les transmet aux agents, les récupère comme confirmations.
- La seule opération permise sur le système de fichiers est **lister le répertoire de travail** si un chemin est absent ou ambigu — jamais ouvrir un fichier.

## Entrées attendues

Fournir dans le prompt d'invocation :

1. **Chemin du document à analyser** — obligatoire. La trame de propale (`trame-{nom-projet}-V{n}.md` ou fichier équivalent). L'orchestrateur transmet ce chemin aux agents ; il ne lit pas ce fichier.
2. **Chemin du fichier contexte** — recommandé. `contexte-{nom-projet}.md`. Même règle : transmis aux agents, jamais lu par l'orchestrateur.
3. **Nom du projet** — utilisé pour nommer les fichiers temporaires et le rapport final. Si absent, le déduire du nom du fichier de trame sans lire son contenu.

## Orchestration

### Phase 1 — Lancement simultané des 3 agents de revue

Effectuer les **3 appels à l'outil Agent dans un seul et même message** (réponse unique), ce qui garantit leur exécution en parallèle. Ne pas attendre la réponse d'un agent avant d'appeler le suivant.

Chaque agent reçoit uniquement des **chemins de fichiers** — jamais de contenu extrait.

---

**Agent 1 — Storytelling**
- Type d'agent : `storytelling-reviewer` (défini dans `${CLAUDE_PLUGIN_ROOT}/agents/storytelling-reviewer.md`)
- Prompt à passer :
  ```
  Nom du projet : [nom-projet]
  Chemin de la trame : [chemin-trame]
  [Si contexte disponible : Chemin du fichier contexte : [chemin-contexte]]
  ```
- Cet agent lit la trame, produit son analyse dans un fichier temporaire `_revue-storytelling-[nom-projet].md` et retourne uniquement une confirmation avec le chemin de ce fichier.

---

**Agent 2 — Cohérence**
- Type d'agent : `coherence-reviewer` (défini dans `${CLAUDE_PLUGIN_ROOT}/agents/coherence-reviewer.md`)
- Prompt à passer :
  ```
  Nom du projet : [nom-projet]
  Chemin de la trame : [chemin-trame]
  [Si contexte disponible : Chemin du fichier contexte : [chemin-contexte]]
  ```
- Cet agent lit la trame, produit son analyse dans un fichier temporaire `_revue-coherence-[nom-projet].md` et retourne uniquement une confirmation avec le chemin de ce fichier.

---

**Agent 3 — Pertinence**
- Type d'agent : `pertinence-reviewer` (défini dans `${CLAUDE_PLUGIN_ROOT}/agents/pertinence-reviewer.md`)
- Prompt à passer :
  ```
  Nom du projet : [nom-projet]
  Chemin de la trame : [chemin-trame]
  [Si contexte disponible : Chemin du fichier contexte : [chemin-contexte]]
  ```
- Cet agent lit la trame, produit son analyse dans un fichier temporaire `_revue-pertinence-[nom-projet].md` et retourne uniquement une confirmation avec le chemin de ce fichier.

---

Attendre la fin des 3 agents. Récupérer les 3 chemins de fichiers temporaires depuis leurs confirmations. Ne pas lire ces fichiers.

### Phase 2 — Synthèse

Lancer l'agent de synthèse avec les 3 chemins de fichiers temporaires :

**Agent 4 — Synthèse**
- Type d'agent : `synthesis-reviewer` (défini dans `${CLAUDE_PLUGIN_ROOT}/agents/synthesis-reviewer.md`)
- Prompt à passer :
  ```
  Nom du projet : [nom-projet]
  Chemin de la trame originale : [chemin-trame]
  Chemin de l'analyse storytelling : [chemin retourné par l'agent 1]
  Chemin de l'analyse cohérence : [chemin retourné par l'agent 2]
  Chemin de l'analyse pertinence : [chemin retourné par l'agent 3]
  ```
- Cet agent lit les 3 fichiers d'analyse, produit le rapport final `revue-[nom-projet].md` et retourne uniquement un résumé : scores des 3 axes, verdict global, chemin du fichier final. L'orchestrateur ne lit pas le fichier final.

### Phase 3 — Clôture

Relayer à l'utilisateur le résumé reçu de l'agent de synthèse :
- Le chemin du fichier final `revue-[nom-projet].md`.
- Les scores des 3 axes (storytelling / cohérence / pertinence).
- Le verdict global en une phrase.

Ne rien ajouter, ne rien reformuler depuis les fichiers — l'orchestrateur ne les a pas lus et ne peut pas les commenter. Le contenu complet est dans le fichier final, que l'utilisateur lira directement.
