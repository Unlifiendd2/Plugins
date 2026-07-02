# orkester-propale-toolbox

Boîte à outils Orkester pour la construction de propositions commerciales (propales). Reprend le meilleur d'`orkester-plugin` et de `propale-review-plugin` autour d'un principe central : un **orchestrateur** dans le fil de discussion principal qui ne touche jamais aux fichiers bruts, et des **sous-agents en contexte frais** qui produisent les fichiers et ne retournent que des résumés.

## Principes

- **Fil principal minimal** — l'orchestrateur `propale-toolbox` manipule des chemins, jamais du contenu. Tout travail de fond est délégué à des sous-agents.
- **Système de session** — le fichier `contexte-{projet}.md` à la racine de l'espace de travail est la source de vérité. Une session peut être reprise depuis une conversation vierge à partir de ce seul fichier et des fichiers produits.
- **Exception d'initialisation** — au premier lancement uniquement, l'orchestrateur lit le fichier de contexte s'il existe, ou lit les fichiers sources (avec garde-fou de taille : au-delà de ~100 pages cumulées, un sous-agent produit le résumé) et crée le fichier de contexte.
- **Deux mécanismes de délégation** — agent dédié pour le cas général ; `skill-executor` uniquement quand la tâche a besoin de la structure d'un skill (références, scripts, assets).

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
orkester-propale-toolbox/
├── .claude-plugin/
│   └── plugin.json               # Manifeste du plugin
├── skills/
│   └── propale-toolbox/
│       └── SKILL.md              # Point d'entrée : orchestrateur de session
├── agents/
│   ├── skill-executor.md         # Exécution de skills en contexte frais
│   ├── trame-reviewer.md         # Orchestrateur de la revue multi-axes (3 + 1 agents)
│   ├── storytelling-reviewer.md  # Axe storytelling → output/tmp/
│   ├── coherence-reviewer.md     # Axe cohérence → output/tmp/
│   ├── pertinence-reviewer.md    # Axe pertinence → output/tmp/
│   └── synthesis-reviewer.md     # Consolidation → output/revue-{projet}.md
└── README.md                     # Ce fichier
```

## Feuille de route

- [x] Skill point d'entrée `propale-toolbox` (orchestration, sessions, initialisation)
- [x] Revue multi-axes indépendante (storytelling, cohérence, pertinence) — agent `trame-reviewer`
- [ ] Création de trame sur mesure
- [ ] Rédaction de sections
