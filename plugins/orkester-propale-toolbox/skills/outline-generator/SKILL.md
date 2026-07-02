---
name: outline-generator
description: >-
  Construit la trame sur-mesure d'une proposition commerciale (propale) Orkester à partir de la
  qualification de la mission (4 axes) du fichier contexte : sélectionne les sections pertinentes
  depuis le catalogue de référence et les rassemble en groupes ordonnés autour d'un fil rouge
  explicite, chaque groupe décrit par son contenu et son objectif. Produit une trame courte et
  synthétique output/trame-{nom-projet}-V{n}.md. À exécuter exclusivement à travers l'agent
  skill-executor, en lui fournissant le chemin du fichier contexte-{projet}.md et la racine de
  l'espace de travail.
---

# Trame de proposition commerciale Orkester

## Ce que fait ce skill

Orkester gagne ses propales en réutilisant un socle de sections récurrentes, mais **toutes les sections n'ont pas leur place dans toutes les propales** : une réponse à appel d'offres pour un nouveau client n'a pas la même structure qu'une offre de TMA pour un client historique. Inclure une section inutile dilue le message ; en oublier une attendue (réversibilité en AO, SLA en TMA, RGPD en B2B…) coûte des points.

Ce skill produit une **trame courte et synthétique** : les sections retenues, rassemblées en groupes ordonnés qui racontent une histoire autour du client (storytelling customer-centric), le tout porté par un **fil rouge explicite**. Chaque groupe est décrit en quelques phrases — son contenu et son objectif dans le récit — sans entrer dans des consignes de rédaction détaillées. Le livrable est un **plan de lecture**, pas une propale rédigée. Il s'appuie sur le catalogue de référence `references/catalogue-sections.md`, qui décrit chaque section, sa raison d'être et sa condition d'inclusion.

Ce skill s'exécute en contexte frais et non-interactif : toutes les informations projet viennent du fichier `contexte-{projet}.md` fourni dans le prompt d'invocation.

## Étape 1 — Récupérer la qualification de la mission (4 axes)

La structure découle de quatre axes, lus dans la section `## Qualification de la mission` du fichier contexte :

1. **Type de mission** — `BUILD` (nouveau projet, refonte, MVP, plateforme à concevoir) ou `RUN` (TMA, TME, reprise de site, maintenance/accompagnement). C'est l'axe le plus structurant. Un build peut inclure un volet maintenance/réversibilité en annexe (cas mixte).
2. **Nature du produit** — `ECOM_B2B`, `ECOM_B2C` ou `APP_MOBILE`. Oriente le vocabulaire, l'architecture et les références à mettre en avant.
3. **Relation client** — `NOUVEAU_CLIENT` (prospect) ou `CLIENT_EXISTANT`.
4. **Contexte commercial** — `APPEL_OFFRES` (formel, concurrentiel) ou `ECHANGE_DIRECT` (suite à réunion).

Si un axe est marqué `À compléter` ou absent, tenter de le déduire du reste du fichier contexte (contexte deal, fichiers sources décrits) et signaler l'hypothèse dans le résumé final. Les axes 1 et 4 changent radicalement le résultat : si l'un des deux est indéductible, c'est un **blocage** — renvoyer la raison et l'information manquante à l'agent invocateur sans produire de trame.

## Étape 2 — Charger le catalogue

Lire `references/catalogue-sections.md`. Il contient les ~35 sections (A à H), leur raison d'être, leur objectif et leur **condition d'inclusion** exprimée en fonction des axes ci-dessus. Cet ordre A→H est **l'ordre de lecture suggéré** d'une propale Orkester ; la trame finale peut modifier cet ordre pour mieux raconter son histoire (storytelling customer-centric).

## Étape 3 — Sélectionner les sections

Pour chaque section du catalogue, évaluer sa condition d'inclusion au regard des 4 axes, puis la classer en **Obligatoire**, **Recommandée** ou **Écartée**. Repères :

- **Toujours incluses** (quel que soit le cas) : A1 page de garde, A3 sommaire, A4 compréhension de la mission, F1 gouvernance, F2 équipe, F3 planning, G1 budget, H3 contact.
- **Bloc cœur selon l'axe 1 :**
  - `BUILD` → activer le bloc **C** (compréhension métier & vision) et le bloc **D** (réponse technique & méthodo agile). Écarter par défaut le bloc E (sauf garantie/TMA en annexe).
  - `RUN` → activer le bloc **E** (E1 TMA, E2 TME si évolutif attendu, E3 SLA toujours, E4 reprise si reprise d'un existant). Le bloc D se réduit à D1 « architecture existante reprise » ; écarter C4/C5/D3/D4/D5.
- **Modulateurs :**
  - `CLIENT_EXISTANT` → activer B5 (pourquoi Orkester) et B6 (historique de la collaboration) ; alléger B1.
  - `NOUVEAU_CLIENT` → activer B1 (qui sommes-nous), B3 (domaines d'intervention), B7 (références) ; écarter B6.
  - `APPEL_OFFRES` → ajouter A2 (édito), E5 (réversibilité), E6 (gestion des risques), H1 (RGPD/sécurité) et étoffer B1.
  - `ECOM_B2B` / grand compte / données sensibles → activer H1 (RGPD/sécurité).
  - Axe 2 → filtrer B4 (technos pertinentes), B7 et H2 (références du bon univers : mobilité vs e-commerce).

En cas de doute sur une section, préférer l'inclure dans son groupe en la signalant comme optionnelle dans la description, plutôt que de la supprimer silencieusement : c'est à l'utilisateur de trancher à la lecture de la trame.

## Étape 4 — Définir le fil rouge, regrouper et ordonner

**Définir le fil rouge** : l'idée-force / promesse-signature qui traverse toute la propale et autour de laquelle le récit s'organise. S'appuyer sur le contexte deal du fichier contexte (fil rouge / promesse-signature, différenciateurs) quand il est renseigné ; sinon le formuler depuis les enjeux du client et le signaler comme hypothèse.

**Regrouper** : rassembler les sections retenues en **groupes cohérents, le moins de groupes possible** (typiquement 5 à 8), chaque groupe portant une étape du récit (ex. « Votre enjeu, notre compréhension », « La vision produit », « Comment nous fabriquons », « Pourquoi nous faire confiance », « Cadre de la mission »…). Une section = un élément d'un groupe, jamais une entrée isolée de la trame, sauf si rien ne peut lui être rattaché.

**Ordonner** les groupes selon un récit centré sur le client, dans lequel il peut s'identifier : ouvrir dans le monde du client avant de parler d'Orkester. Deux ajustements utiles :
- Si `CLIENT_EXISTANT`, remonter l'historique de la relation (B5/B6) en tête de récit pour capitaliser d'emblée sur la relation.
- Les sections de réassurance lourdes d'un `BUILD`/`APPEL_OFFRES` (réversibilité, risques, RGPD, outils) se rassemblent volontiers dans un groupe de fin de corps ou en annexe, pour ne pas casser le fil de l'offre.

## Étape 5 — Produire la sortie

Générer `output/trame-{nom-projet}-V{n}.md` dans la racine de l'espace de travail (créer le dossier `output/` s'il n'existe pas). Pour le numéro de version `{n}`, lister les fichiers `output/trame-{nom-projet}-V*.md` existants et prendre le numéro suivant (V1 s'il n'y en a aucun — ne jamais écraser une version existante).

Ce fichier contient uniquement la trame — la qualification vit dans le fichier contexte. La sortie est **courte et synthétique** : pas de codes de section, pas de consignes « À rédiger » détaillées. Restituer dans ce format :

```
# Trame proposée — {nom-projet} V{n}

**Fil rouge :** <la promesse-signature en une phrase, qui traverse tous les groupes>

## 1. <Titre du groupe>
*Objectif : <une phrase — ce que ce groupe doit produire chez le lecteur : convaincre, rassurer, projeter, prouver…>*

<2 à 3 phrases concises sur le contenu du groupe : les sections qu'il rassemble et les points clés à couvrir, contextualisés pour CE client (nom, produit, secteur, solution quand ils sont connus). Signaler ici les éléments optionnels.>

## 2. ...

## Sections écartées
- <Titre> — <raison courte liée aux axes>
```

Les descriptions de groupes doivent rester **spécifiques** au cas — citer le client, le produit, le secteur — mais tenir en 2-3 phrases : la trame entière doit se lire d'un coup d'œil.

## Quand consulter la base orkester-kb

Par défaut, le catalogue suffit : **ne pas interroger la base de connaissance**. Y recourir uniquement si l'un de ces cas se présente :

- une **ambiguïté** que les 4 axes ne lèvent pas (ex. type de produit hybride, périmètre flou entre build et reprise) et que le fichier contexte ne tranche pas ;
- un **scénario non couvert** par le catalogue (ex. mission de conseil pur, audit, cadrage seul, formation, produit d'un secteur inhabituel) pour lequel il faut vérifier comment Orkester a structuré une propale comparable.

Dans ce cas, utiliser les outils MCP `Orkester-kb` : `search_kb_semantic` ou `search_kb_hybrid` pour retrouver des passages pertinents des propales gagnées (sources `propale_*.md`), puis `get_full_document` pour récupérer la structure complète d'une propale proche. En extraire les sections manquantes, les intégrer à la trame, et signaler dans le résumé final qu'elles proviennent d'un cas réel hors catalogue.
