# Orkester — Marketplace de plugins Claude Code

Ce dépôt est une **marketplace de plugins Claude Code** pour Orkester. Il regroupe deux briques :

1. **`plugins/`** — les plugins Claude Code (skills + sous-agents).
2. **`BDD_vectorielle/`** — la base de connaissances, exposée aux plugins via un serveur MCP (`orkester-kb`).

## Plugins

| Plugin | Rôle | Orkester-kb |
| --- | --- | --- |
| [orkester-propale-toolbox](plugins/orkester-propale-toolbox/) | Boîte à outils complète et à jour le 20/08/26 : orchestration par sous-agents, espace de travail sessionné, fil principal minimal | Requis |
| [orkester-propale-toolbox-no-mcp](plugins/orkester-propale-toolbox-no-mcp/) | Même boîte à outils (version du 24/07/26), **sans** accès à la base de connaissances | Non |
| [propale-review-plugin](plugins/propale-review-plugin/) | Revue indépendante d'une trame selon trois axes parallèles (storytelling, cohérence, pertinence) + synthèse | Non |
| [orkester-plugin](plugins/orkester-plugin/) | Première génération de skills propale (`propale-maker`, `propale-base-creator`, `identity-creator`, `base-reviewer`) — antérieur à la toolbox | Requis |

Chaque plugin a son propre README détaillant ses skills, ses agents et sa feuille de route.

### orkester-propale-toolbox — le plugin de référence

C'est le plugin présenté.

Outils couverts : couverture fonctionnelle, relevé des TJM par profil, chiffrage, génération de trame, revue de trame 3 lentilles.

Documentation : [Doc orkester-propale-toolbox](https://orkester.atlassian.net/wiki/spaces/AIO/pages/937328641/Documentation+technique+fonctionnelle+orkester-propale-toolbox+au+19+08+26)

## Base de connaissances vectorielle (`BDD_vectorielle/`)

![Python](https://img.shields.io/badge/python-3.12.10-blue?logo=python&logoColor=white)

Indexation des propales gagnées d'Orkester dans [ChromaDB](https://www.trychroma.com/), exposée aux agents via un serveur MCP nommé **`orkester-kb`**.

### Fichiers

| Fichier | Rôle |
| --- | --- |
| [docling-test.py](BDD_vectorielle/docling-test.py) | Conversion PDF → Markdown via Docling, avec OCR (fr/en) du texte et des images |
| [ingest.py](BDD_vectorielle/ingest.py) | Chunking des Markdown (découpage sur les titres `## `, overlap, 512 tokens max) et ingestion dans la collection `propales` |
| [chroma_mcp.py](BDD_vectorielle/chroma_mcp.py) | Serveur MCP FastMCP exposant 5 outils de recherche sur la base |
| [scripts.py](BDD_vectorielle/scripts.py) | Aide-mémoire de snippets Chroma (requêtes, suppression de collection, listing des sources) |
| [output/](BDD_vectorielle/output/) | Propales converties en Markdown, source de l'ingestion |
| [chroma/](BDD_vectorielle/chroma/) | Données persistées de ChromaDB |

Embeddings : `intfloat/multilingual-e5-base` (convention e5, préfixe `passage: `), distance cosinus.

### Outils MCP exposés

- `search_kb_semantic` — recherche sémantique
- `search_kb_keyword` — recherche par mots-clés exacts, classée par nombre de correspondances
- `search_kb_hybrid` — sémantique + filtrage par mots-clés
- `get_full_document` — réassemble un document complet depuis son nom de source (overlaps retirés)
- `get_adjacent_chunks` — contexte autour d'un chunk donné

### Mise en route

```bash
cd BDD_vectorielle
pip install -r requirements.txt

# 1. Lancer ChromaDB (localhost:8000)
chroma run

# 2. Ingérer les Markdown de output/ dans la collection "propales"
py ingest.py

# 3. Lancer le serveur MCP (HTTP, 127.0.0.1:9000)
py chroma_mcp.py
```

Le serveur doit ensuite être enregistré auprès de Claude Code sous le nom **`orkester-kb`** — les agents référencent explicitement les outils `mcp__orkester-kb__*`. Dans Claude code :

```bash
claude mcp add --transport http orkester-kb http://127.0.0.1:9000/mcp
```

Dans Claude desktop, dans `claude_desktop_config.json` ajouter :

```json
  "mcpServers": {
    "orkester-kb": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://127.0.0.1:9000/mcp"
      ]
    }
  }
```

Sans ce serveur, les plugins `orkester-propale-toolbox` et `orkester-plugin` ne fonctionnent pas correctement ; utiliser `orkester-propale-toolbox-no-mcp` dans ce cas.

> Note : `ingest.py` lit les Markdown de `output/` en **UTF-16**, encodage produit par `docling-test.py`. Un fichier ajouté manuellement doit respecter cet encodage.

## Structure du dépôt

```
Plugins/
├── .claude-plugin/
│   └── marketplace.json                  # Manifeste de la marketplace (4 plugins)
├── plugins/
│   ├── orkester-propale-toolbox/         # Plugin de référence (avec Orkester-kb)
│   ├── orkester-propale-toolbox-no-mcp/  # Variante sans base de connaissances
│   ├── propale-review-plugin/            # Revue de trame 3 axes + synthèse
│   └── orkester-plugin/                  # Première génération de skills propale
├── BDD_vectorielle/                      # Base vectorielle + serveur MCP orkester-kb
└── README.md                             # Ce fichier
```
