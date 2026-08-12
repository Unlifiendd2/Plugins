---
name: pricing-estimator
description: >-
  Produit le chiffrage d'une proposition commerciale Orkester à partir d'une couverture
  fonctionnelle : estime la charge de chaque fonction par profil, applique la grille de TJM relevée
  dans orkester-kb, ajoute les charges transverses (cadrage, gestion de projet, recette, garantie)
  et consolide en un budget par brique puis global. Produit un tableau où chaque ligne de la
  couverture devient une ligne de charge et de montant, dans
  output/chiffrage-{nom-projet}-V{n}.md. Isole systématiquement les fonctions non validées
  (déduites, à confirmer) dans un sous-total distinct. Orchestré par le skill propale-toolbox
  (jamais invoqué directement) et exécuté à travers l'agent skill-executor, en lui fournissant les
  chemins de la couverture fonctionnelle, de output/tmp/tjm-orkester.md, de output/contexte.md et
  la racine de l'espace de travail.
---

# Chiffrage

## Ce que fait ce skill

La couverture fonctionnelle a établi **ce qu'il y a à faire**, une ligne par fonction. Ce skill lui adosse **combien ça coûte** : une charge par profil pour chaque fonction, les taux de la grille TJM, les charges transverses, et la consolidation.

Le principe directeur est la **traçabilité ligne à ligne** : chaque référence de la couverture (`PORT-01`) se retrouve dans le chiffrage avec sa charge et son montant. On doit pouvoir remonter d'un total à la fonction qui le porte, et inversement — c'est ce qui permet de discuter un budget avec un client sans le refaire.

**Ce que ce skill ne fait pas** : il ne redéfinit pas le périmètre (la couverture fait foi), n'invente pas de taux (la grille TJM fait foi), et ne décide pas de la marge commerciale ni des remises — ce sont des arbitrages de direction, pas de méthode.

Ce skill s'exécute en contexte frais et non-interactif.

## Étape 1 — Rassembler la matière

1. **La couverture fonctionnelle** `output/couverture-fonctionnelle-{projet}-V{n}.md` — la version dont le chemin est fourni dans le prompt d'invocation. C'est le périmètre : ne rien ajouter, ne rien retirer. Relever son numéro de version, il devra figurer en tête du chiffrage.
2. **La grille TJM** `output/tmp/tjm-orkester.md` — les taux et leur niveau de confiance. Si elle est absente du prompt, le signaler comme blocage plutôt que d'inventer des taux.
3. **`output/contexte.md`** — le périmètre, les contraintes de budget et de délai, les enjeux. Un chiffrage qui ignore une contrainte budgétaire annoncée par le client est un chiffrage inutile.

Ne pas ouvrir les fichiers sources : tout ce qui est nécessaire est dans ces trois fichiers. Si un point manque, aller dans les résumés `output/tmp/resume-*.md`.

## Étape 2 — Choisir les profils du chiffrage

Retenir **3 à 6 profils** parmi ceux de la grille TJM, ceux que le projet mobilise réellement. Ils deviendront les colonnes du tableau. Une colonne par profil marginal alourdit la lecture sans rien apporter : regrouper plutôt que multiplier.

Repères de sélection : un profil de pilotage, un ou deux profils de conception (cadrage / UX), un ou deux profils de réalisation (back, front, mobile selon le produit), un profil de recette. Ajouter un profil spécialisé (architecte, data, IA, DevOps) uniquement si le projet en dépend explicitement.

Si un profil nécessaire est marqué `Non trouvé` dans la grille : ne pas inventer son taux. Le chiffrer en charge (jours) sans montant, laisser la cellule montant vide, et le remonter en blocage partiel dans le résumé final.

## Étape 3 — Estimer la charge de chaque fonction

Pour chaque ligne de la couverture, estimer une charge en jours par profil retenu. La colonne « Précisions pour le chiffrage » de la couverture porte ce qui pèse : volumétrie, complexité, dépendance à un tiers — s'en servir.

**Le calibrage ne s'invente pas.** Lire `references/methode-chiffrage.md` : il fixe la démarche, l'échelle de complexité et le traitement des charges transverses. En cas de doute sur l'ordre de grandeur d'une fonction, chercher dans `orkester-kb` une propale comparable et s'aligner sur son calibrage plutôt que sur une intuition — puis le signaler.

Trois règles fermes :

- **Une fonction, une ligne, une charge.** Ne jamais fondre deux fonctions dans une estimation commune : on perdrait la traçabilité qui fait la valeur du document.
- **L'intégration d'un service tiers se chiffre à part de son interface.** « Smart scan IA » côté portail et côté Mistral sont deux lignes de la couverture : deux charges distinctes, jamais mutualisées.
- **Aucune charge à zéro.** Si une fonction ne coûte rien, elle n'est pas une fonction — la signaler dans les hypothèses plutôt que de l'inscrire à 0.

## Étape 4 — Isoler ce qui n'est pas validé

C'est le point sur lequel un chiffrage se joue en revue interne. Les fonctions de statut `Déduite` et `À confirmer` portent une charge que le client n'a pas validée.

- Les chiffrer normalement, ligne par ligne, dans leur brique.
- Mais les **exclure du sous-total engagé** et les consolider dans un sous-total distinct : « sous réserve de validation ».
- Le budget global présente donc trois nombres : le **socle** (fonctions explicites), le **sous réserve** (déduites + à confirmer), et le **total** si tout est retenu.

Les fonctions listées « Hors périmètre » dans la couverture ne se chiffrent pas. Les reporter dans une table « Non chiffré » avec leur raison : ce que la propale exclut doit rester visible.

## Étape 5 — Ajouter les charges transverses

Les fonctions ne font pas le projet. Ajouter les lignes transverses décrites dans `references/methode-chiffrage.md` : cadrage, gestion de projet, recette et qualification, mise en production et DevOps, documentation et formation, garantie, aléas. Reprendre aussi les « Éléments transverses » relevés dans la couverture (reprise de données, environnements, RGPD, accessibilité, multilingue…) : ce sont des lignes de charge à part entière.

Chaque ligne transverse indique **sa base de calcul** (« 12 % de la charge de réalisation », « forfait 15 j ») et, quand le taux appliqué n'est pas attesté par `orkester-kb`, une mention explicite qu'il s'agit d'une hypothèse à valider. Un pourcentage posé sans justification ne se distingue pas d'un chiffre inventé.

## Étape 6 — Produire la sortie

Générer `output/chiffrage-{nom-projet}-V{n}.md` dans la racine de l'espace de travail. Pour le numéro de version, lister les `output/chiffrage-{nom-projet}-V*.md` existants et prendre le suivant (V1 s'il n'y en a aucun — ne jamais écraser).

```markdown
# Chiffrage — {nom-projet} V{n}

> Établi sur la couverture fonctionnelle {V{m}} et la grille TJM du {…}.
> Socle engagé : {montant} € · Sous réserve de validation : {montant} € · Total : {montant} €
> Charge totale : {N} jours.

## Profils et taux appliqués

| Profil | TJM appliqué | Confiance | Rôle sur le projet |
|---|---|---|---|
| {Profil} | {montant} € | {Élevée/Moyenne/Faible} | {une ligne} |

## {Brique}

| Réf | Fonction | Statut | {Profil A} | {Profil B} | {Profil C} | Charge (j) | Montant |
|---|---|---|---|---|---|---|---|
| PORT-01 | Authentification | Explicite | 1 | 4 | 1 | 6 | {montant} € |
| PORT-03 | Gestion des droits | Déduite | 1 | 3 | 1 | 5 | {montant} € |
| | **Sous-total brique** | | | | | **{N} j** | **{montant} €** |

## {Brique suivante}
...

## Charges transverses

| Poste | Base de calcul | Charge (j) | Montant |
|---|---|---|---|
| Cadrage | {forfait / % } | {N} | {montant} € |
| Gestion de projet | {…} | {N} | {montant} € |
| Recette et qualification | {…} | {N} | {montant} € |
| {Élément transverse repris de la couverture} | {…} | {N} | {montant} € |
| Aléas | {…} | {N} | {montant} € |

## Synthèse

| Poste | Charge (j) | Montant |
|---|---|---|
| {Brique} | {N} | {montant} € |
| ... | | |
| Charges transverses | {N} | {montant} € |
| **Socle engagé** | **{N}** | **{montant} €** |
| Sous réserve de validation | {N} | {montant} € |
| **Total si tout est retenu** | **{N}** | **{montant} €** |

## Non chiffré

| Réf | Fonction | Raison |
|---|---|---|

## Hypothèses et points de vigilance

- {Hypothèse de calibrage, taux non attesté, profil manquant, dépendance externe non maîtrisée, écart à une contrainte budgétaire annoncée.}
```

Règles de sortie :

- **Les références de la couverture sont reprises à l'identique.** Une ligne du chiffrage sans réf correspondante dans la couverture est une erreur — sauf les charges transverses, qui n'en ont pas.
- **Toute fonction de la couverture apparaît**, y compris celles à charge faible. Un chiffrage partiel se repère mal et se corrige tard.
- Les montants s'écrivent en euros entiers, sans décimale. Les charges en jours, par pas de 0,5.
- Si une contrainte de budget figure dans `output/contexte.md` et que le total la dépasse, **le dire dans les points de vigilance** avec l'écart chiffré. Ne jamais raboter silencieusement des charges pour atteindre une cible : c'est à l'utilisateur d'arbitrer.

## Itération

Relancé, ce skill **repart de la couverture fonctionnelle la plus récente** et produit une V{n+1}. Un chiffrage ne s'édite pas à la main : ses totaux dépendent de chaque ligne, et une retouche isolée les rend faux.

Si la demande consiste à ajuster un calibrage ou un taux, l'appliquer et recalculer l'ensemble. Si elle consiste à changer le périmètre, c'est la **couverture** qu'il faut reprendre d'abord — le signaler comme blocage plutôt que de chiffrer un périmètre qui n'existe dans aucun document.
