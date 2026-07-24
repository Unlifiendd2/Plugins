# orkester-propale-toolbox-no-mcp

Boîte à outils Orkester pour la construction de propositions commerciales (propales) — **version sans MCP**, identique à `orkester-propale-toolbox` mais sans aucun accès à la base de connaissances `Orkester-kb`. Reprend le meilleur d'`orkester-plugin` et de `propale-review-plugin` autour d'un principe central : un **orchestrateur** dans le fil de discussion principal qui délègue la production des fichiers à des **sous-agents en contexte frais**, lesquels ne retournent que des résumés.

## Principes

- **Fil principal minimal** — l'orchestrateur `propale-toolbox` délègue toute production de fichiers aux sous-agents et relaie leurs résumés. Il ne lit les fichiers produits que quand un échange avec l'utilisateur nécessite des informations qu'ils contiennent.
- **Système de session** — le fichier `contexte-{projet}.md` à la racine de l'espace de travail est la source de vérité. Une session peut être reprise depuis une conversation vierge à partir de ce seul fichier et des fichiers produits.
- **Sécurité de taille** — avant de lire des fichiers fournis par l'utilisateur, vérification de leur taille : au-delà de ~100 pages cumulées (ou format binaire), un sous-agent générique produit un résumé structuré à la place.
- **Deux mécanismes de délégation** — agent dédié pour le cas général ; `skill-executor` uniquement quand la tâche a besoin de la structure d'un skill (références, scripts, assets).
- **Sans MCP / sans Orkester-kb** — aucun agent de ce plugin n'accède à une base de connaissances externe. Le travail s'appuie uniquement sur les fichiers sources fournis, le fichier contexte et le catalogue de sections intégré (`outline-generator`).

## Structure de l'espace de travail

```
{dossier de travail}/
├── contexte-{projet}.md      # Source de vérité de la session
├── {fichiers sources}        # Fichiers ajoutés par l'utilisateur
├── output/
│   ├── tmp/                  # Fichiers temporaires des sous-agents
│   └── …                     # Livrables à destination de l'utilisateur
└── artifact/                 # Fichiers finaux complets (fin de session)
```

## Structure du plugin

```
orkester-propale-toolbox-no-mcp/
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
│   ├── context-initializer.md    # Init de session : synthèse des sources d'input
│   ├── skill-executor.md         # Exécution de skills en contexte frais
│   └── trame-reviewer.md         # Revue de trame 3 lentilles → output/revue-{projet}.md
└── README.md                     # Ce fichier
```

## Feuille de route

- [x] Skill point d'entrée `propale-toolbox` (orchestration, sessions, initialisation)
- [x] Création de trame sur mesure — skill `outline-generator` (via `skill-executor`)
- [x] Revue de trame 3 lentilles (storytelling, cohérence, pertinence) — agent `trame-reviewer`
- [ ] Rédaction de sections
