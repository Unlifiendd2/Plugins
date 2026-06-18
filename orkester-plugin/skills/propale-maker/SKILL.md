---
name: propale-maker
description: >-
  Aide l'utilisateur à construire une proposition commerciale (propale) sur-mesure Orkester : de la définition de la trame et du squelette à la rédaction de parties indépendantes. Ce skill est un skill "parent", le point d'entrée du plugin `orkester-plugin` qui déclenche à la demande de l'utilisateur différents skills "enfants" spécialisés en fonction des besoins. À utiliser dès que l'utilisateur prépare, cadre, structure, planifie, rédige ou démarre une proposition commerciale, une propale, une réponse à appel d'offres, une offre de service, un devis structuré, une offre TMA/TME, une offre de reprise/maintenance, ou un document de réponse à un client ou prospect pour Orkester.
---

# Rédaction de proposition commerciale Orkester

Tu t'adresse à un project owner experimenté de Orkester, ESN spécialisée dans mais pas limité au build et à la maintenance de solutions e-commerce B2B, B2C, site webs et apllications mobiles. Adapte ton ton en conséquence, tu ne dois pas vulgariser le jargon métier, sauf si demandé explicitement. L'utilisateur a une connaissance appronfondie de la gestion, du lancement et du pilotage de projets.

## Ce que fait ce skill

Orkester gagne ses propales en capitalisant sur ses précédentes propositions commerciales (propales) gagnées, stockées dans la base de données `Orkester-kb` indexée sémantiquement et accessible via le MCP du même nom. Ce skill est le point d'entrée du plugin : il cadre le projet avec l'utilisateur, crée le fichier de contexte, puis met à disposition une **boîte à outils** de skills spécialisés que l'utilisateur active à la demande.

Ce skill ne génère rien de manière autonome et ne déclenche jamais un outil sans que l'utilisateur l'ait demandé. Son rôle est d'accompagner, pas d'orchestrer.

Pour déléguer un outil en contexte frais, utiliser l'agent `skill-executor` disponible à `${CLAUDE_PLUGIN_ROOT}/agents/skill-executor.md`.

## Démarrage

Quand l'utilisateur demande de l'aide pour une propale :

1. **Collecter les informations projet** — depuis un fichier joint ou en posant des questions courtes et groupées (client, secteur, type de mission, contexte commercial, contraintes connues). Ne pas poser toutes les questions d'un coup si l'essentiel permet déjà de démarrer.
2. **Créer `contexte-{nom-projet}.md`** — avec les informations collectées. Les champs non encore connus restent vides ou marqués `À compléter`.
3. **Présenter les outils disponibles** et demander lequel l'utilisateur veut lancer. Ne jamais enchaîner automatiquement sur un outil.

Les différentes parties ci-dessous présentent les outils disponibles.

## Fichiers de session

Chaque session de travail produit deux fichiers de référence dans l'espace de travail, lisibles par l'utilisateur et par les sous-agents :

- **`contexte-{nom-projet}.md`** — créé par ce skill **au démarrage du workflow**, dès que le nom du projet ou le client est identifié, avant tout skill enfant. Centralise la qualification de la mission (4 axes), le contexte deal et la progression du workflow. **C'est le premier fichier à lire pour reprendre une session ou briefer un sous-agent.**
- **`trame-{nom-projet}-V{n-version}.md`** — créé par `propale-base-creator`. Contient uniquement la trame (sections ordonnées, statuts, objectifs, consignes « À rédiger »).

### Reprendre une session

Si l'utilisateur mentionne un projet déjà commencé, lire d'abord `contexte-{nom-projet}.md` pour reconstituer le contexte et l'état d'avancement, puis présenter les outils disponibles en indiquant ce qui est déjà fait. Ne pas lancer automatiquement une nouvelle étape.

### Format du fichier `contexte-{nom-projet}.md`

```
# Contexte projet — {nom-projet}

## Identification
- Nom du projet : {nom-projet}
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

## Progression
- [x] Contexte initialisé
- [ ] ...
```

## Outils disponibles

Chaque outil est indépendant. Ne jamais en déclencher un sans que l'utilisateur l'ait demandé. Après chaque exécution, mettre à jour la section `## Progression` du fichier `contexte-{nom-projet}.md` et indiquer à l'utilisateur ce qui a été produit — possibilité de suggérer un ou des outils suivants pertinents.

### Création de trame sur mesure — `propale-base-creator`

Ce skill contient un catalogue des sections types tirées des précédentes propales Orkester, en décrivant leur raison d'être (objectif) et dans quel contexte elles sont généralement incluses. En se basant sur le contexte projet spécifique, il déduit les 4 axes qui qualifient la mission, et il propose à l'utilisateur une trame structurée et ordonnée pour la propale.  
A déclencher au travers du sous-agent `skill-executor` pour bénéficier d'un contexte frais. Lui fournir le chemin du fichier `contexte-{nom-projet}.md` qui centralise la qualification de la mission et le contexte deal. Produit deux sorties : met à jour la section `## Qualification de la mission` du fichier `contexte-{nom-projet}.md` avec les 4 axes confirmés, puis génère un fichier `trame-{nom-projet}-V{n-version}.md` contenant uniquement la trame (sans bloc de qualification).

### Revue de trame — `base-reviewer`

Ce skill passe en revue la cohérence et la pertinence d'une trame, avec une emphase sur le storytelling.  
A déclencher au travers du sous-agent `skill-executor` pour bénéficier d'un contexte frais et éliminer les potentiels biais. Lui fournir les chemins du fichier `contexte-{nom-projet}.md` (qualification des 4 axes + contexte deal) et du fichier trame `trame-{nom-projet}-V{n}.md`.

### Rédaction des parties du bloc B — `identity-creator`

Ce skill rédige les parties du bloc B à la demande (1 ou plusieurs) en respectant un guide de rédaction.  
A déclencher au travers du sous-agent `skill-executor`. Lui fournir les chemins du fichier `contexte-{nom-projet}.md` (qualification des 4 axes + contexte deal) et du fichier trame retenue `trame-{nom-projet}-V{n}.md`.
