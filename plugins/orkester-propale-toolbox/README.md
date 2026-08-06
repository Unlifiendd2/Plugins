# orkester-propale-toolbox

Boîte à outils Orkester pour la construction de propositions commerciales (propales). Reprend le meilleur d'`orkester-plugin` et de `propale-review-plugin` autour d'un principe central : un **orchestrateur** dans le fil de discussion principal qui délègue la production des fichiers à des **sous-agents en contexte frais**, lesquels ne retournent que des résumés.

## Principes

- **Fil principal minimal** — l'orchestrateur `propale-toolbox` délègue toute production de fichiers aux sous-agents et relaie leurs résumés. Il ne lit les fichiers produits que quand un échange avec l'utilisateur nécessite des informations qu'ils contiennent.
- **Délégation de l'accès à la donnée** — le fil principal ne lit **jamais** les fichiers sources déposés par l'utilisateur, quels que soient leur taille et leur format. Un sous-agent en produit un résumé structuré par source dans `output/tmp/` ; c'est sur ces résumés que Claude construit sa compréhension du projet.
- **Système de session** — `progression.md` à la racine de l'espace de travail est la source de vérité. Une session peut être reprise depuis une conversation vierge à partir de ce seul fichier et des fichiers produits.
- **Socle de la propale** — `output/contexte.md` (contexte, objectifs, enjeux, périmètre, précédents) met au clair la raison d'être du projet et la lecture qu'Orkester en fait. Il est co-écrit par Claude et l'utilisateur, et sert de base à tous les livrables suivants.
- **Deux mécanismes de délégation** — agent dédié pour le cas général ; `skill-executor` uniquement quand la tâche a besoin de la structure d'un skill (références, scripts, assets).
- **Accès à Orkester-kb** — tous les agents du plugin ont accès via MCP à la base vectorielle des propales gagnées d'Orkester, pour ancrer leur travail dans les pratiques qui ont fait leurs preuves.

## Structure de l'espace de travail

```
{dossier de travail}/
├── progression.md            # Source de vérité de la session
├── {fichiers sources}        # Déposés par l'utilisateur — jamais lus par le fil principal
├── output/
│   ├── contexte.md           # Socle de la propale (co-écrit avec l'utilisateur)
│   ├── tmp/                  # Résumés des sources + intermédiaires des sous-agents
│   └── …                     # Autres livrables (trames, revues…)
└── artifact/                 # Fichiers finaux complets (fin de session)
```

## Structure du plugin

```
orkester-propale-toolbox/
├── .claude-plugin/
│   └── plugin.json               # Manifeste du plugin
├── skills/
│   ├── propale-toolbox/
│   │   └── SKILL.md              # Point d'entrée : orchestrateur de session
│   ├── outline-generator/
│   │   ├── SKILL.md              # Création de trame → output/trame-{projet}-V{n}.md
│   │   └── references/
│   │       └── catalogue-sections.md  # Catalogue des ~35 sections types (A à H)
│   └── propale-toolbox-help/
│       └── SKILL.md              # Documentation de référence du plugin
├── agents/
│   ├── context-initializer.md    # Init de session : résumés des sources + Orkester-kb + progression.md
│   ├── skill-executor.md         # Exécution de skills en contexte frais
│   └── trame-reviewer.md         # Revue de trame 3 lentilles → output/revue-{projet}.md
└── README.md                     # Ce fichier
```

## Feuille de route

- [x] Skill point d'entrée `propale-toolbox` (orchestration, sessions, initialisation)
- [x] Création de trame sur mesure — skill `outline-generator` (via `skill-executor`)
- [x] Revue de trame 3 lentilles (storytelling, cohérence, pertinence) — agent `trame-reviewer`
- [ ] Rédaction de sections
