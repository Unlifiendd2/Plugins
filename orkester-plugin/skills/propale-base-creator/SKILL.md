---
name: propale-base-creator
description: >-
  Construit la trame sur-mesure d'une proposition commerciale (propale) Orkester : qualifie la mission selon 4 axes (build/run, nature du produit, relation client, contexte commercial), puis sélectionne et ordonne les sections à inclure en donnant pour chacune son objectif et des consignes de rédaction. A déclencher qu'à partir du skill propale-maker.
---

# Trame de proposition commerciale Orkester

## Ce que fait ce skill

Orkester gagne ses propales en réutilisant un socle de sections récurrentes, mais **toutes les sections n'ont pas leur place dans toutes les propales** : une réponse à appel d'offres pour un nouveau client n'a pas la même structure qu'une offre de TMA pour un client historique. Inclure une section inutile dilue le message ; en oublier une attendue (réversibilité en AO, SLA en TMA, RGPD en B2B…) coûte des points.

Ce skill produit une **trame ordonnée et justifiée** : la liste des sections à inclure, dans le bon ordre, chacune accompagnée de son objectif et de consignes de rédaction adaptées au cas précis. Il met l'emphase sur une trame qui raconte une histoire autour du client (storytelling customer-centric). Le livrable est un **plan à remplir**, pas une propale rédigée. Il s'appuie sur le catalogue de référence `${CLAUDE_PLUGIN_ROOT}/skills/propale-base-creator.md`, qui décrit chaque section, sa raison d'être et sa condition d'inclusion.

## Étape 1 — Qualifier la mission (4 axes)

La structure découle de quatre axes. Si un fichier `contexte-{nom-projet}.md` est disponible, le lire pour récupérer les axes déjà qualifiés. Pour les axes manquants, **poser des questions courtes et groupées** à l'utilisateur (ne pas lancer la trame sur des hypothèses silencieuses, car l'axe 1 et l'axe 4 changent radicalement le résultat).

1. **Type de mission** — `BUILD` (nouveau projet, refonte, MVP, plateforme à concevoir) ou `RUN` (TMA, TME, reprise de site, maintenance/accompagnement). C'est l'axe le plus structurant. Un build peut inclure un volet maintenance/réversibilité en annexe (cas mixte).
2. **Nature du produit** — `ECOM_B2B`, `ECOM_B2C` ou `APP_MOBILE`. Oriente le vocabulaire, l'architecture et les références à mettre en avant.
3. **Relation client** — `NOUVEAU_CLIENT` (prospect) ou `CLIENT_EXISTANT`.
4. **Contexte commercial** — `APPEL_OFFRES` (formel, concurrentiel) ou `ECHANGE_DIRECT` (suite à réunion).

Si l'utilisateur fournit peu d'éléments, ces quatre axes suffisent à démarrer : les demander explicitement est presque toujours le meilleur premier pas.

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

En cas de doute sur une section, préférer **Recommandée** (avec une note) plutôt que de la supprimer silencieusement : c'est à l'utilisateur de trancher.

## Étape 4 — Ordonner

Proposer un ordre basé sur un fil rouge qui porte tout le document autour d'une histoire centrée sur le client dans laquelle il peut s'identifier. Ouvrir le récit dans le monde du client avant de parler de Orkester.  

Deux ajustements utiles :
- Si `CLIENT_EXISTANT`, placer B5/B6 juste après le sommaire (avant la compréhension de la mission) pour capitaliser d'emblée sur la relation.
- Les sections de réassurance lourdes d'un `BUILD`/`APPEL_OFFRES` (E5 réversibilité, E6 risques, H1 RGPD, F4 outils) se placent volontiers en fin de corps ou en annexe, pour ne pas casser le fil de l'offre.

## Étape 5 — Produire la sortie

Deux actions dans cet ordre :

**1. Mettre à jour `contexte-{nom-projet}.md`**  
Renseigner la section `## Qualification de la mission` avec les 4 axes confirmés, et cocher la case `Trame créée` dans la `## Progression`.

**2. Générer `trame-{nom-projet}-V{n-version}.md`**  
Ce fichier contient uniquement la trame — la qualification vit dans le fichier contexte. Restituer dans ce format :

```
## Trame proposée — {nom-projet} V{n}

1. [Code] Titre de la section — *Statut : Obligatoire|Recommandée*
   - Objectif : <une phrase, tirée du catalogue>
   - À rédiger : <2 à 4 puces concrètes, adaptées à CE client / contexte (pas génériques)>
2. ...

## Sections écartées (et pourquoi)
- [Code] Titre — <raison courte liée aux axes>
```

Les consignes « À rédiger » doivent être **spécifiques** au cas : citer le nom du client, le produit, la solution technique, le secteur quand ils sont connus. Une consigne générique (« présenter l'équipe ») apporte peu ; une consigne contextualisée (« présenter l'équipe mobile Flutter et son expérience parfumerie/cosmétique ») guide vraiment la rédaction.

## Quand consulter la base orkester-kb

Par défaut, le catalogue suffit : **ne pas interroger la base de connaissance**. Y recourir uniquement si l'un de ces cas se présente :

- une **ambiguïté** que les 4 axes ne lèvent pas (ex. type de produit hybride, périmètre flou entre build et reprise) et que l'utilisateur ne peut pas trancher ;
- un **scénario non couvert** par le catalogue (ex. mission de conseil pur, audit, cadrage seul, formation, produit d'un secteur inhabituel) pour lequel il faut vérifier comment Orkester a structuré une propale comparable.

Dans ce cas, utiliser les outils MCP `Orkester-kb` : `search_kb_semantic` ou `search_kb_hybrid` pour retrouver des passages pertinents des propales gagnées (sources `propale_*.md`), puis `get_full_document` pour récupérer la structure complète d'une propale proche. En extraire les sections manquantes, les intégrer à la trame, et signaler à l'utilisateur qu'elles proviennent d'un cas réel hors catalogue.
