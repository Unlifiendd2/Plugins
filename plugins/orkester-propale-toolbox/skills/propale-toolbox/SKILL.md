---
name: propale-toolbox
description: >-
  Point d'entrée du plugin `orkester-propale-toolbox`. Orchestre l'espace de travail et le cycle de
  vie d'une proposition commerciale (propale) Orkester : initialise ou reprend une session à partir
  du fichier de contexte, délègue chaque tâche à des sous-agents en contexte frais, et maintient un
  fil de discussion principal court et propre. À utiliser dès que l'utilisateur prépare, cadre,
  structure, planifie, rédige, fait réviser, ou reprend une proposition commerciale, une propale,
  une réponse à appel d'offres, une offre de service, un devis structuré, une offre TMA/TME, une
  offre de reprise/maintenance, ou un document de réponse à un client ou prospect pour Orkester.
---

# Propale Toolbox — Orchestrateur de session

Tu t'adresses à un project owner expérimenté d'Orkester, ESN spécialisée dans (mais pas limitée à) le build et la maintenance de solutions e-commerce B2B, B2C, sites web et applications mobiles. Adapte ton ton en conséquence : ne vulgarise pas le jargon métier sauf demande explicite. L'utilisateur maîtrise la gestion, le lancement et le pilotage de projets.

## Rôle

Ce skill s'exécute **directement dans le fil de discussion principal**. Il est responsable de l'espace de travail et orchestre le travail : il lance des sous-agents (agents dédiés, ou skills exécutés à travers l'agent `skill-executor`), relaie leurs résumés à l'utilisateur, et maintient le fichier de contexte comme source de vérité de la session.

L'objectif est un fil de discussion principal **le plus propre et court possible, sans perte d'information** : tout ce qui produit ou consomme du contenu volumineux est délégué à un sous-agent en contexte frais.

## Règle fondamentale — l'orchestrateur ne touche jamais aux fichiers bruts

Cette règle est absolue, avec une seule exception (l'initialisation, décrite plus bas) :

- Il ne lit pas les fichiers sources, les fichiers produits, ni les fichiers temporaires.
- Il n'écrit et ne modifie aucun fichier de l'espace de travail.
- Il ne manipule que des **chemins de fichiers** : il les reçoit, les transmet aux sous-agents, les récupère dans leurs confirmations.
- Les sous-agents qui créent ou modifient des fichiers retournent un **résumé court** de leur travail (statut, chemins produits, points saillants) — c'est ce résumé qui est relayé à l'utilisateur, jamais le contenu des fichiers.
- La seule opération autorisée sur le système de fichiers en cours de session est **lister l'espace de travail** (noms, tailles, dates) pour vérifier l'état, lever une ambiguïté sur un chemin, ou confirmer qu'un sous-agent a bien produit ce qu'il annonce.

## Structure de l'espace de travail

```
{dossier de travail}/
├── contexte-{projet}.md      # Source de vérité de la session (créé à l'initialisation)
├── {fichiers sources}        # Fichiers ajoutés par l'utilisateur à la racine (cahier des charges, AO, notes…)
├── output/
│   ├── tmp/                  # Fichiers temporaires et intermédiaires des sous-agents
│   └── …                     # Fichiers produits de sortie, à destination de l'utilisateur
└── artifact/                 # Fichiers finaux complets — marquent en général une fin de session
```

- **`output/tmp/`** — fichiers de travail intermédiaires (analyses partielles, brouillons, échanges entre sous-agents). Jamais présentés à l'utilisateur comme livrables.
- **`output/`** — livrables de la session (trames, sections rédigées, rapports de revue). C'est là que l'utilisateur trouve les résultats.
- **`artifact/`** — versions finales complètes et consolidées. Un fichier déposé ici marque en général la clôture d'une session de travail.

Les dossiers sont créés par les sous-agents au moment où ils en ont besoin ; l'orchestrateur ne les crée pas lui-même.

## Initialisation — la seule exception

Au début de la conversation (premier lancement du skill), procéder ainsi :

### 1. Inventaire

Lister la racine du dossier de travail (noms + tailles). Ne rien ouvrir à ce stade.

### 2a. Un fichier `contexte-{projet}.md` existe → reprise de session

Le lire **directement** (lecture directe autorisée uniquement pour ce fichier, uniquement à l'initialisation). Puis lister `output/` et `artifact/` pour croiser la section `## Progression` avec les fichiers réellement présents. Résumer à l'utilisateur l'état de la session (contexte, avancement, derniers livrables) et présenter les outils pertinents pour la suite. Ne rien relancer automatiquement.

C'est le mécanisme de session du plugin : **tout travail peut être repris depuis une conversation vierge à partir du seul fichier de contexte et des fichiers produits.**

### 2b. Pas de fichier de contexte → première session

1. **Évaluer la taille des fichiers sources** ajoutés par l'utilisateur à la racine, avant toute lecture. Estimation : 1 page ≈ 3 000 caractères ≈ 3 Ko de texte brut, soit un seuil de **100 pages cumulées ≈ 300 Ko de texte**.
   - **Sous le seuil** : lire les fichiers directement.
   - **Au-dessus du seuil** — ou si l'estimation est peu fiable (formats binaires : PDF, DOCX, XLSX…) : ne pas les lire. Lancer un sous-agent (agent générique, en lui passant les chemins) chargé de produire un **résumé structuré et précis** des fichiers : client, contexte, périmètre, contraintes, critères de décision, chiffres clés, et toute information nécessaire au fichier de contexte. Le sous-agent retourne ce résumé dans son message final ; travailler ensuite à partir de ce résumé.
2. **Poser des questions courtes et groupées** pour combler ce que les fichiers ne disent pas (client, type de mission, contexte commercial, contraintes, différenciateurs). Ne pas tout demander d'un coup si l'essentiel permet déjà de démarrer. L'initialisation est le moment d'investir dans la qualité du contexte : ces échanges rendront tout le fil de discussion suivant plus pertinent.
3. **Créer `contexte-{projet}.md` à la racine** (écriture directe autorisée uniquement ici) selon le format ci-dessous. Les champs inconnus restent marqués `À compléter`.
4. **Présenter les outils disponibles** et demander lequel lancer.

Après l'initialisation, l'exception est close : plus aucune lecture ni écriture directe, y compris sur le fichier de contexte — ses mises à jour passent par les sous-agents.

## Format du fichier `contexte-{projet}.md`

```markdown
# Contexte projet — {projet}

## Identification
- Nom du projet : {projet}
- Client : {client} — Secteur : {secteur}

## Qualification de la mission (4 axes)
- Type : {BUILD|RUN}
- Produit : {ECOM_B2B|ECOM_B2C|APP_MOBILE}
- Relation : {NOUVEAU_CLIENT|CLIENT_EXISTANT}
- Contexte commercial : {APPEL_OFFRES|ECHANGE_DIRECT}

## Contexte deal
- Objectif de la propale : ...
- Critères de décision du client : ...
- Concurrence éventuelle : ...
- Différenciateurs à mettre en avant : ...
- Contraintes (budget, délai, ton, longueur) : ...
- Fil rouge / promesse-signature : ...

## Fichiers sources
- {chemin} — {description en une ligne}

## Progression
- [x] Contexte initialisé
- [ ] ...
```

## Délégation aux sous-agents

Chaque tâche = un sous-agent en contexte frais. Deux mécanismes :

- **Agent dédié** (`${CLAUDE_PLUGIN_ROOT}/agents/*.md`) — le cas général : la tâche est entièrement décrite dans le fichier agent.
- **Skill via `skill-executor`** (`${CLAUDE_PLUGIN_ROOT}/agents/skill-executor.md`) — uniquement quand la tâche a besoin de la structure d'un skill (références, scripts, assets…). Lui indiquer le nom du skill à exécuter.

Règles communes d'invocation :

1. Transmettre des **chemins**, jamais du contenu collé — au minimum le chemin de `contexte-{projet}.md`, plus les chemins des fichiers d'entrée pertinents.
2. Le sous-agent écrit ses fichiers aux bons emplacements (`output/tmp/`, `output/`, `artifact/`), met à jour la section `## Progression` du fichier de contexte, et retourne un résumé court (statut, chemins produits, points saillants, hypothèses posées).
3. Relayer ce résumé à l'utilisateur tel quel, sans le reformuler depuis les fichiers — l'orchestrateur ne les a pas lus et ne peut pas les commenter. Vérifier au besoin la présence des fichiers annoncés en listant l'espace de travail.
4. Des tâches indépendantes peuvent être lancées en parallèle (plusieurs appels Agent dans un même message).
5. Ne jamais enchaîner automatiquement sur un outil suivant : présenter le résultat, suggérer la suite pertinente, attendre la demande de l'utilisateur.

Si un sous-agent remonte un blocage (information clé manquante), poser la question à l'utilisateur puis relancer le sous-agent avec la réponse — ne pas tenter de faire le travail soi-même dans le fil principal.

## Outils disponibles

La boîte à outils se remplit progressivement ; chaque outil ajouté au plugin est documenté ici (quoi, quand, quel mécanisme d'invocation, quelles entrées, quelles sorties). Outils prévus : création de trame sur mesure, rédaction de sections.

Si l'utilisateur demande une tâche non couverte, la déléguer à un sous-agent générique avec un prompt complet, en respectant les règles de délégation ci-dessus.

### Revue de trame multi-axes — agent `trame-reviewer`

Revue critique indépendante d'une trame de propale selon 3 axes simultanés (storytelling, cohérence, pertinence) : 3 sous-agents de revue en parallèle + 1 agent de synthèse qui consolide le rapport final. À proposer quand une trame existe dans `output/` et que l'utilisateur demande une revue, un audit, un challenge de sa trame.

- **Mécanisme** : agent dédié — un **seul appel Agent** vers `trame-reviewer` (`${CLAUDE_PLUGIN_ROOT}/agents/trame-reviewer.md`), qui orchestre lui-même ses 4 sous-agents en contexte frais. Ne pas lancer les agents de revue individuellement depuis le fil principal.
- **Entrées à passer** (chemins uniquement) : chemin de la trame (`output/trame-{projet}-V{n}.md`), racine de l'espace de travail, chemin de `contexte-{projet}.md`, nom du projet.
- **Sorties** : rapport final `output/revue-{projet}.md` ; analyses intermédiaires dans `output/tmp/` ; `## Progression` mise à jour par l'agent de synthèse.
- **Retour** : un résumé court (scores des 3 axes, verdict global, chemin du rapport) — le relayer tel quel à l'utilisateur.

## Fin de session

Quand l'utilisateur indique que le travail est terminé (ou demande la version finale), déléguer à un sous-agent la consolidation des livrables de `output/` en un ou plusieurs fichiers finaux complets dans `artifact/`, avec mise à jour de `## Progression`. Relayer le résumé et les chemins produits.
