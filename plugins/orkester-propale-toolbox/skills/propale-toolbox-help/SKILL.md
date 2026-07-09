---
name: propale-toolbox-help
description: >-
  Documentation de référence du plugin `orkester-propale-toolbox`. À utiliser pour répondre aux
  questions de l'utilisateur ou pour récolter des informations sur le plugin : comment l'utiliser, quels outils existent et quand
  les lancer, comment fonctionnent les sessions et l'espace de travail, quels sont les détails
  techniques (agents, skills, délégation), les bonnes pratiques, et comment réagir en cas de
  problème (fichier manquant, référence à un fichier introuvable, session à reprendre, blocage
  d'un sous-agent). À déclencher quand l'utilisateur demande de l'aide, « comment ça marche »,
  « que peux-tu faire », « à quoi sert ce plugin », pose une question sur son fonctionnement,
  quand une erreur est rencontrée dans le workflow de propale-toolbox, quand l'utilisateur
  utilise mal le plugin (ex. demande une trame ou un livrable sur un espace de travail vierge,
  sans cahier des charges ni brief), ou quand Claude peine à réaliser une tâche demandée.
---

# Aide — plugin `orkester-propale-toolbox`

Ce skill est la **référence unique** pour répondre aux questions sur le plugin. Il ne produit aucun fichier et ne lance aucun outil : il sert à expliquer, orienter et dépanner. Après avoir répondu, si l'utilisateur veut agir, revenir au fonctionnement normal (skill `propale-toolbox`, qui orchestre).

Répondre de façon ciblée à la question posée — ne pas déverser toute la documentation. Piocher la section pertinente ci-dessous.

## En une phrase

Le plugin aide un project owner Orkester à construire une proposition commerciale (propale) de bout en bout — cadrage, trame, revue, consolidation — en gardant le fil de discussion principal court et propre : un **orchestrateur** dialogue avec l'utilisateur et **délègue** tout le travail de fond à des **sous-agents en contexte frais** qui produisent les fichiers.

## Comment l'utiliser — le cycle de vie type

1. **Démarrer** — ouvrir une conversation dans le dossier de travail (idéalement avec les fichiers sources : cahier des charges, AO, notes, à la racine). Le skill `propale-toolbox` s'initialise : soit il lit un contexte existant (reprise), soit, en première session, il délègue à l'agent `context-initializer` qui synthétise les sources, cherche dans `Orkester-kb` les projets/clients/secteurs déjà traités par Orkester, et crée `contexte-{projet}.md` ; l'orchestrateur complète ensuite avec quelques questions ciblées.
2. **Structurer** — définir le fil rouge avec l'orchestrateur (proposé puis challengé), puis lancer `outline-generator` pour produire la trame (`output/trame-{projet}-V{n}.md`).
3. **Réviser** — lancer `trame-reviewer` pour une revue critique 3 lentilles (`output/revue-{projet}.md`), itérer sur la trame si besoin (nouvelle version V{n+1}).
4. **Consolider** — en fin de session, déléguer la consolidation des livrables de `output/` vers un fichier final dans `artifact/`.

À chaque étape, l'orchestrateur présente le résultat et **suggère** la suite sans jamais l'enchaîner automatiquement : c'est l'utilisateur qui décide de l'outil suivant.

## Les outils disponibles

| Outil | Rôle | Mécanisme | Sortie |
|---|---|---|---|
| `outline-generator` (skill) | Construit la trame synthétique (fil rouge + groupes de sections) | via `skill-executor` | `output/trame-{projet}-V{n}.md` |
| `trame-reviewer` (agent) | Revue critique 3 lentilles : storytelling, cohérence, pertinence | appel Agent direct | `output/revue-{projet}.md` |

Outils prévus (feuille de route) : rédaction de sections. Pour toute tâche non couverte, l'orchestrateur délègue à un sous-agent générique avec un prompt complet.

## Le principe central — fil principal propre, délégation systématique

- L'orchestrateur (`propale-toolbox`) vit **dans le fil principal**. Il ne crée/modifie **jamais** de fichier de travail lui-même (seule exception : `contexte-{projet}.md` à l'initialisation).
- Toute production de contenu est **déléguée à un sous-agent en contexte frais**, qui écrit les fichiers et ne retourne qu'un **résumé court** (statut, chemins, points saillants, hypothèses). C'est ce résumé qui est relayé.
- L'orchestrateur peut **lister** l'espace de travail à volonté, et **lire** un fichier produit uniquement quand un échange avec l'utilisateur le nécessite (répondre à une question, comparer des versions, citer un passage) — pas pour produire.
- **Pourquoi** : un fil principal court reste pertinent, rapide et peu coûteux ; les sous-agents en contexte frais évitent les biais d'accumulation et isolent chaque tâche.

## Le système de session

- `contexte-{projet}.md`, à la racine, est la **source de vérité** : identification, qualification de la mission (4 axes), contexte deal, fil rouge, liste des fichiers sources, et `## Progression`.
- **Toute session est reprenable depuis une conversation vierge** à partir du seul fichier de contexte + des fichiers produits. À la réouverture, l'orchestrateur lit le contexte, croise la `## Progression` avec les fichiers réellement présents, et résume l'état.
- Les sous-agents mettent à jour le contexte (progression, enrichissements) au fil de leurs tâches — l'orchestrateur ne le réécrit pas après l'initialisation.

### Les 4 axes de qualification de la mission

Ils structurent toute la propale : **Type** (`BUILD` / `RUN`), **Produit** (`ECOM_B2B` / `ECOM_B2C` / `APP_MOBILE`), **Relation** (`NOUVEAU_CLIENT` / `CLIENT_EXISTANT`), **Contexte commercial** (`APPEL_OFFRES` / `ECHANGE_DIRECT`). Les axes 1 (Type) et 4 (Contexte commercial) sont les plus structurants : sans eux, `outline-generator` se bloque plutôt que de deviner.

## Architecture technique

```
orkester-propale-toolbox/
├── skills/
│   ├── propale-toolbox/     # Orchestrateur, point d'entrée (fil principal)
│   ├── outline-generator/   # Création de trame (+ references/catalogue-sections.md)
│   └── propale-toolbox-help/ # Ce skill de documentation
└── agents/
    ├── context-initializer.md # Init de session : synthèse des sources + recherche Orkester-kb
    ├── skill-executor.md    # Exécute un skill en contexte frais (accès Orkester-kb)
    └── trame-reviewer.md    # Revue 3 lentilles en contexte frais (accès Orkester-kb)
```

- **Deux mécanismes de délégation** : *agent dédié* (cas général, tâche décrite dans le fichier agent) ; *skill via `skill-executor`* (uniquement quand la tâche a besoin de la structure d'un skill : références, scripts, assets — comme le catalogue de sections d'`outline-generator`).
- **Orkester-kb** : base vectorielle des propales gagnées d'Orkester, accessible via MCP par **tous les sous-agents** (jamais par le fil principal). Elle sert à ancrer le travail dans les pratiques éprouvées.
- **Espace de travail** : `output/tmp/` (intermédiaires), `output/` (livrables), `artifact/` (finaux complets, fin de session).

## Bonnes pratiques

- **Fournir les sources au démarrage** — poser les fichiers (AO, cahier des charges, notes) à la racine avant d'initialiser : le contexte n'en sera que plus riche.
- **Investir dans le contexte et le fil rouge** — ce sont les deux moments où l'interaction utilisateur a le plus de valeur ; tout le reste en découle. Challenger le fil rouge plutôt que d'accepter la première formulation.
- **Une version par itération** — les trames sont versionnées (`V1`, `V2`…) et jamais écrasées. Réviser produit une nouvelle version, ce qui garde l'historique.
- **Laisser les sous-agents faire le gros** — ne pas demander à l'orchestrateur de rédiger ou d'analyser lui-même dans le fil principal ; c'est le rôle des sous-agents.
- **Reprendre proprement** — pour continuer un projet, rouvrir une conversation dans le même dossier ; inutile de tout recontextualiser à la main, le fichier de contexte s'en charge.

## Dépannage — comment réagir

**L'utilisateur demande un livrable (trame, revue…) avec un espace de travail vierge et aucun input.**
C'est le cas de mauvaise utilisation le plus fréquent. **Ne pas lancer un long questionnaire** pour reconstituer un cahier des charges à la main : ce n'est pas ainsi que le plugin est conçu. Expliquer brièvement le point d'entrée attendu et demander à l'utilisateur de fournir la matière première :
- soit **déposer un cahier des charges / appel d'offres / brief** à la racine de l'espace de travail,
- soit **le joindre directement à la conversation**.

Une fois la source disponible, l'initialisation se déroule normalement (lecture des sources → quelques questions ciblées seulement sur ce qui manque → création du contexte). Quelques questions de cadrage restent utiles ; c'est le questionnaire exhaustif en l'absence totale de source qu'il faut éviter. Si l'utilisateur n'a réellement aucun document, le lui dire clairement : un minimum d'éléments (client, type de mission, contexte commercial) est nécessaire pour produire quoi que ce soit de pertinent.

**Claude peine à réaliser une tâche / n'est pas sûr de la marche à suivre.**
Ne pas improviser ni forcer un résultat approximatif. Faire un pas en arrière : vérifier l'état réel de l'espace de travail (listing), le contexte disponible, et l'outil approprié à la demande (voir le tableau des outils). Si la demande sort du périmètre du plugin, le dire et proposer l'alternative la plus proche. Si un input manque, le demander précisément plutôt que de deviner. En cas de doute sur le fonctionnement lui-même, s'appuyer sur ce présent skill.

**Aucun `contexte-{projet}.md` trouvé alors que l'utilisateur parle d'un projet existant.**
Lister la racine et les sous-dossiers pour repérer un contexte nommé différemment ou placé ailleurs. Si vraiment absent : soit on est en première session (initialiser normalement), soit le fichier a été perdu — le reconstruire à partir des fichiers produits présents (`output/`, `artifact/`) et de quelques questions ciblées, puis reprendre.

**L'utilisateur référence un fichier introuvable** (trame, revue, source…).
Ne pas inventer son contenu. Lister l'espace de travail et proposer les fichiers réellement présents dont le nom est proche. Vérifier une éventuelle confusion de version (`V1` vs `V2`) ou de dossier (`output/` vs `output/tmp/` vs `artifact/`). Si le fichier attendu n'existe pas, l'expliquer et proposer de le (re)générer avec l'outil adéquat.

**Un sous-agent remonte un blocage** (information clé manquante).
Relayer clairement la raison du blocage et l'information manquante, poser la question à l'utilisateur, puis **relancer le sous-agent** avec la réponse. Ne pas tenter de faire le travail à la place dans le fil principal.

**Les 4 axes ne sont pas qualifiés / `outline-generator` se bloque.**
Les axes 1 (BUILD/RUN) et 4 (AO/échange direct) sont indispensables. Les demander explicitement à l'utilisateur, mettre à jour le contexte, puis relancer.

**Fichiers sources trop volumineux** (> ~100 pages cumulées, ou PDF/DOCX/XLSX).
Ne pas les charger dans le fil principal. Déléguer à un sous-agent générique un résumé structuré, et travailler à partir de ce résumé.

**La `## Progression` ne correspond pas aux fichiers présents.**
Se fier aux fichiers réellement présents (vérité terrain) plutôt qu'à la case cochée. Signaler l'écart à l'utilisateur et proposer de resynchroniser (relancer l'étape manquante ou corriger la progression via un sous-agent).

**L'utilisateur veut une info précise contenue dans un livrable.**
C'est un cas légitime de lecture directe par le fil principal : lire le fichier concerné, répondre à la question, sans recopier tout le contenu dans le fil.

## Limites connues

- Le fil principal n'a pas accès à `Orkester-kb` : la proposition de fil rouge s'appuie sur le contexte projet déjà consolidé, pas sur une recherche live dans les propales gagnées. Pour un ancrage KB, déléguer une recherche préparatoire à un sous-agent.
- Le plugin couvre aujourd'hui le cadrage, la trame et la revue ; la rédaction fine des sections reste à venir.
