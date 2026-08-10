---
name: functional-coverage
description: >-
  Décompose les documents sources d'un projet en couverture fonctionnelle : la liste des fonctions
  à réaliser, regroupées par brique de la solution (applications, services tiers intégrés, socle
  technique). Le niveau de granularité visé n'est ni l'epic ni la user story, mais la fonction —
  une capacité autonome, désignée par un groupe nominal court, chiffrable d'un bloc. Produit
  output/couverture-fonctionnelle-{nom-projet}-V{n}.md, base de travail de l'estimation budgétaire.
  Orchestré par le skill propale-toolbox (jamais invoqué directement) et exécuté à travers l'agent
  skill-executor, en lui fournissant les chemins de output/contexte.md, des résumés de output/tmp/,
  des fichiers sources et la racine de l'espace de travail.
---

# Couverture fonctionnelle

## Ce que fait ce skill

Une propale se chiffre à partir de ce qu'il y a à construire. Avant de poser des charges, il faut donc arrêter **la liste des fonctions que la solution doit couvrir** — ni un découpage projet (epics), ni une expression de besoin détaillée (user stories), mais l'inventaire des capacités fonctionnelles, groupées par brique de la solution.

C'est un document court, plat et lisible d'un coup d'œil : on doit pouvoir le poser devant le client et lui faire dire « oui, c'est bien ça » ou « il manque X ». C'est aussi la base de travail du chiffrage : chaque ligne est une charge à estimer.

**Ce que ce skill ne fait pas** : il ne chiffre pas (ni jours, ni euros, ni complexité), ne rédige pas de user stories, ne produit pas de découpage en lots ou en sprints, et ne propose pas d'architecture technique. Il établit le périmètre fonctionnel, rien d'autre.

Ce skill s'exécute en contexte frais et non-interactif.

## Étape 1 — Rassembler la matière

Dans cet ordre :

1. **`output/contexte.md`** — le socle de la propale. Sa section `## Périmètre` fixe ce qui est dedans et ce qui n'y est pas ; `## Objectifs` et `## Enjeux` disent ce que la solution doit permettre. C'est la référence qui arbitre en cas de doute.
2. **Les résumés `output/tmp/resume-*.md`** — la synthèse de chaque source.
3. **Les fichiers sources eux-mêmes** — les ouvrir. Contrairement aux autres tâches du plugin, celle-ci exige un relevé **exhaustif** : une fonction oubliée est une charge oubliée dans le chiffrage. Les résumés donnent la structure, les sources donnent le détail. Cette lecture est permise ici parce qu'elle a lieu en contexte frais, dans un sous-agent — jamais dans le fil principal.

Si les fichiers sources ne sont pas fournis dans le prompt d'invocation, travailler depuis les résumés et le contexte, et **signaler dans le résumé final** que la couverture est établie sans relecture des sources — donc à valider de près.

### Comment lire les sources

**Lire les fichiers soi-même, en un appel `Read` par fichier.** Ne jamais déléguer la lecture, l'extraction ou la conversion d'une source à un sous-agent : faire extraire un PDF en JSON par un agent, puis faire reformater ce JSON par un second, enchaîne des allers-retours coûteux pour un résultat que `Read` rend directement.

Pour un **PDF**, appeler `Read` **sans le paramètre `pages`**, avec le seul chemin du fichier — même sur un document volumineux, et même si la description de l'outil laisse entendre que `pages` est requis au-delà de 10 pages. L'appel par défaut rend le document entier nativement, texte et images comprises. Le paramètre `pages` déclenche un rendu page par page via `pdftoppm` (poppler), absent de cet environnement : il échoue sur `pdftoppm is not installed`, sans repli possible faute d'accès au shell.

Si une source reste illisible malgré cela, ne pas la contourner : remonter le blocage et le chemin du fichier concerné dans le résumé final.

## Étape 2 — Identifier les briques de la solution

Une brique est un ensemble cohérent qui se conçoit, se construit et se chiffre comme un tout. Les repérer avant de lister quoi que ce soit — c'est le découpage qui rend la couverture lisible.

Quatre familles, dans cet ordre :

1. **Les applications et interfaces**, une par population d'utilisateurs ou par canal : portail client, back-office / dashboard admin, application mobile, front public, extranet partenaire. C'est le gros de la couverture.
2. **Les services tiers intégrés**, un groupe par service nommé (Stripe, Mistral AI, Brevo, un ERP, un PIM, un CRM, un transporteur, un service d'identité…). On y liste ce que **l'intégration** doit couvrir, pas les capacités du service lui-même.
3. **Le socle technique**, uniquement s'il porte des fonctions identifiables : hébergement et stockage de médias, exports et téléchargements, traitements par lots, supervision. Ne pas en faire un fourre-tout d'infrastructure.
4. **La reprise de l'existant**, quand il y en a une : migration de données, reprise de contenus, bascule.

Nommer chaque brique avec le vocabulaire du projet tel qu'il apparaît dans les sources (« Portail offre autonome », « Dashboard admin ») plutôt qu'avec un terme générique.

## Étape 3 — Lister les fonctions

### La granularité — la règle centrale

Une **fonction** est une capacité fonctionnelle autonome de la solution, qu'on peut chiffrer d'un bloc.

- **Au-dessus** se trouve la brique (« Portail client ») : c'est un regroupement, pas une fonction.
- **Au-dessous** se trouve la user story (« en tant que client, je peux modifier mon adresse de facturation ») : c'est un détail d'une fonction, absorbé par elle.

Quatre tests pour se caler :

- **Test du chiffrage** — peut-on lui associer une charge sans avoir à la redécouper d'abord ? Si le chiffrage exige de la casser en morceaux, elle est trop grosse.
- **Test du nom** — se nomme-t-elle par un groupe nominal de 2 à 5 mots, sans « et » ni énumération ? Un nom qui contient « et » cache presque toujours deux fonctions.
- **Test de l'absence** — si elle n'était pas livrée, quelqu'un s'en apercevrait-il ? Si non, c'est un détail d'implémentation, pas une fonction.
- **Test de l'ordre de grandeur** — une brique applicative porte typiquement 8 à 20 fonctions, un service tiers 2 à 6. Une brique à 40 lignes est trop découpée ; à 3 lignes, trop agrégée.

### La formulation

- **Groupe nominal**, jamais de phrase ni de verbe conjugué : « Génération de facture », pas « Le système génère une facture ».
- **Le vocabulaire du client** tel qu'il apparaît dans les sources : « Vérification de SIRET », « Auto-immatriculation INPI », « Chasseur de charges ». Une couverture fonctionnelle doit être reconnaissable par celui qui a écrit le cahier des charges — ne pas traduire son métier en termes génériques.
- **Le CRUD se regroupe** : « Gestion des données clients » plutôt que quatre lignes créer / consulter / modifier / supprimer.
- **Pas de mention de la technique** : « Suggestion d'adresse », pas « Intégration de l'API Google Places ». La technologie se dit dans la brique de service tiers, pas dans le nom de la fonction.

### Les répétitions entre briques sont normales

Une même capacité peut apparaître dans deux briques — « Authentification » dans le portail **et** dans le dashboard admin, « Smart scan IA recettes » côté portail **et** côté service Mistral AI. Ce ne sont pas des doublons : ce sont deux charges distinctes, l'interface d'un côté, l'intégration de l'autre. Les conserver, et ne jamais dédoublonner silencieusement.

## Étape 4 — Challenger la couverture

Lire `references/repertoire-fonctions.md` : il recense les fonctions qui reviennent d'un projet à l'autre, par domaine, avec leur condition de pertinence. Le passer en revue **après** avoir listé ce que disent les sources, et jamais avant — il sert à repérer les oublis, pas à générer la liste.

Pour chaque fonction du répertoire pertinente au regard des axes du projet (Type, Produit, Relation, Contexte commercial) mais absente de la liste : soit elle a été omise par les sources et il faut l'ajouter comme **déduite**, soit elle est hors périmètre et il faut le dire explicitement. Un cahier des charges omet presque toujours l'administration des utilisateurs, la reprise de données, les exports et la gestion des droits — ce sont les oublis les plus coûteux au chiffrage.

## Étape 5 — Statuer sur chaque fonction

Quatre statuts. Seuls les trois derniers s'écrivent ; l'explicite est le cas par défaut, non annoté.

- **Explicite** — demandée dans les sources. Rien à signaler.
- **Déduite** — non demandée, mais nécessaire pour que la solution tienne debout. À marquer *(déduite)*. Ne jamais glisser une fonction déduite sans le dire : elle porte une charge que le client n'a pas demandée et qu'il devra accepter.
- **À confirmer** — mentionnée de façon ambiguë, ou dont le périmètre n'est pas tranché. À marquer *(à confirmer)*, et à reprendre dans les zones d'ombre avec la question à poser.
- **Hors périmètre** — évoquée puis exclue, repoussée à une phase ultérieure, ou couverte par le client / un autre prestataire. À lister à part : dans une propale, ce qui est exclu doit être aussi visible que ce qui est inclus.

## Étape 6 — Produire la sortie

Générer `output/couverture-fonctionnelle-{nom-projet}-V{n}.md` dans la racine de l'espace de travail (créer le dossier `output/` s'il n'existe pas). Pour le numéro de version `{n}`, lister les fichiers `output/couverture-fonctionnelle-{nom-projet}-V*.md` existants et prendre le numéro suivant (V1 s'il n'y en a aucun — ne jamais écraser une version existante).

```markdown
# Couverture fonctionnelle — {nom-projet} V{n}

> {Une phrase : ce que couvre la solution, pour qui.}
> Ce document recense les fonctions à réaliser. Il ne les chiffre pas.

## {Brique}
*{Une ligne : rôle de la brique dans la solution, utilisateurs concernés.}*

- {Fonction}
- {Fonction} *(déduite)*
- {Fonction} *(à confirmer)*

## {Brique suivante}
...

## Hors périmètre
- {Fonction} — {exclue par le client / phase ultérieure / à la charge d'un tiers}

## Précisions utiles au chiffrage
- {Brique} · {Fonction} — {ce qui pèse : volumétrie, complexité, dépendance à un tiers, incertitude}

## Éléments transverses (hors fonctions)
- {Ce qui portera de la charge sans être une fonction : reprise de données, nombre d'environnements, exigences RGPD ou d'accessibilité, multilingue, performance, recette, reprise de l'historique, formation, documentation.}

## Zones d'ombre
- {Ce qui empêche de trancher — et la question précise à poser au client.}
```

Règles de sortie :

- Le corps du document — les briques et leurs listes — reste **nu et présentable** : une fonction par ligne, sans commentaire, hormis les marqueurs *(déduite)* et *(à confirmer)*. Tout le reste va dans les sections de fin.
- « Précisions utiles au chiffrage » ne reprend **que** les fonctions qui le méritent (charge inhabituelle, dépendance externe, périmètre incertain) — pas la liste entière.
- Omettre une section de fin plutôt que d'écrire « néant » — sauf « Hors périmètre » et « Zones d'ombre », qu'on renseigne explicitement même vides (« Aucune exclusion identifiée », « Aucune zone d'ombre »), car leur silence serait ambigu.
- Ne rien inventer : une fonction sans appui dans les sources est soit déduite et marquée comme telle, soit absente.

## Itération

Ce skill est relancé quand un amendement de la couverture demande un jugement, une planification ou une relecture des sources — les retouches simples dictées par l'utilisateur (renommer, déplacer, retirer une fonction, réordonner des briques) sont appliquées directement par l'orchestrateur, sans passer par ici.

Dans ce cas :

1. **Partir de la dernière version existante**, telle qu'elle est sur le disque. Elle a pu être amendée à la main par l'orchestrateur depuis la génération précédente : **ces amendements font foi**. Ne jamais régénérer depuis les seules sources en écrasant des arbitrages déjà pris — repérer les écarts, les conserver, et ne retoucher que ce que la demande impose.
2. **Traiter la demande** transmise dans le prompt d'invocation, en revenant aux sources et au répertoire autant que nécessaire.
3. **Produire une nouvelle version** V{n+1}, sans jamais écraser la précédente.

Les retours de l'utilisateur priment sur la déduction depuis les sources : il connaît le deal et ce qui a été dit au client. Si l'un de ses retours contredit frontalement une source, l'appliquer quand même et le signaler dans le résumé final.

## Quand consulter la base orkester-kb

Par défaut, les sources et le répertoire suffisent : **ne pas interroger la base de connaissance**. Y recourir uniquement dans deux cas :

- un **domaine métier inhabituel** dont les sources supposent le vocabulaire connu, et pour lequel il faut vérifier comment Orkester a découpé un projet comparable ;
- un **doute sur le grain** d'une brique entière (trop agrégée ou trop fine par rapport aux usages Orkester).

Dans ce cas, utiliser `search_kb_semantic` ou `search_kb_hybrid` pour retrouver les passages de chiffrage ou de périmètre des propales gagnées (sources `propale_*.md`), puis `get_full_document` si une correspondance mérite d'être lue en entier. Signaler dans le résumé final ce qui a été repris d'un cas réel.
