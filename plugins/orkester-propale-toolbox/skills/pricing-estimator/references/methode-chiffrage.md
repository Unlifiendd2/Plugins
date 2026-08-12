# Méthode de chiffrage

Ce référentiel fixe la **démarche** d'estimation, pas des valeurs Orkester. Les ordres de grandeur qu'il donne sont des repères de calibrage explicitement signalés comme tels : la référence, quand elle existe, se trouve dans `orkester-kb` — une propale comparable et son chiffrage réel valent mieux que n'importe quel abaque.

---

## 1. Les profils

Un chiffrage Orkester mobilise typiquement ces familles. Les intitulés exacts et leurs taux viennent de la grille `output/tmp/tjm-orkester.md` ; ne retenir que ceux que le projet mobilise réellement.

| Famille | Ce qu'elle porte |
|---|---|
| Pilotage | Direction de projet, chefferie de projet, coordination client |
| Cadrage / produit | Product owner, AMOA, ateliers, spécification, backlog |
| Conception | UX, UI, design system, maquettage, prototypage |
| Architecture | Architecture technique, choix de socle, sécurité, performance |
| Réalisation | Développement back, front, mobile, intégration de services tiers |
| Qualité | Recette, tests automatisés, qualification, correction |
| Exploitation | DevOps, environnements, CI/CD, mise en production, supervision |
| Spécialités | Data, IA, SEO, accessibilité, expertise plateforme |

**Regrouper plutôt que multiplier** : au-delà de six colonnes, le tableau devient illisible et la précision affichée devient trompeuse.

## 2. Estimer une fonction

### La démarche, dans l'ordre

1. **Chercher un précédent.** Une fonction comparable a probablement déjà été chiffrée dans une propale Orkester. C'est la source la plus fiable — bien plus qu'une échelle abstraite.
2. **À défaut, classer par complexité**, puis convertir en jours à l'aide d'une échelle posée explicitement pour ce projet.
3. **Ventiler par profil** : une fonction consomme rarement un seul profil. Une fonction d'interface mobilise conception + front + recette ; une intégration mobilise architecture + back + recette.
4. **Signaler l'incertitude** plutôt que de la noyer dans un chiffre rond.

### L'échelle de complexité

Quatre niveaux, à calibrer projet par projet — les jours indiqués ci-dessous sont un **exemple de format**, pas une norme Orkester :

| Niveau | Ce qui le caractérise | Exemple d'ordre de grandeur |
|---|---|---|
| S | Comportement standard, pas de règle métier propre, pas de dépendance | 1–3 j |
| M | Quelques règles métier, un écran ou un flux, données simples | 4–8 j |
| L | Règles métier denses, plusieurs états, dépendance à un tiers ou à des données existantes | 9–15 j |
| XL | Sous-système à part entière, forte incertitude, contraintes de performance ou de conformité | > 15 j — envisager de le remonter à la couverture pour découpage |

Une fonction `XL` est souvent le signe d'un défaut de la couverture : elle agrège plusieurs capacités. Le signaler dans les hypothèses.

### Ce qui fait grossir une charge

- **Les états intermédiaires** — brouillons, validations, annulations, reprises de saisie.
- **Les droits** — une fonction qui se comporte différemment selon le rôle coûte plus qu'une fonction unique.
- **La reprise de données** — alimenter une fonction depuis un existant coûte souvent plus que la fonction elle-même.
- **La gestion d'erreur des tiers** — rejeux, réconciliation, alertes : la moitié de la charge d'une intégration.
- **La volumétrie** — pagination, performance, traitement par lots.

## 3. Les charges transverses

Elles ne sont portées par aucune fonction mais font partie du projet. Chaque ligne doit indiquer **sa base de calcul**, et signaler quand le taux appliqué n'est pas attesté par `orkester-kb`.

| Poste | Base habituelle | À retenir |
|---|---|---|
| Cadrage | Forfait, calé sur le nombre d'ateliers | Croît avec le nombre d'interlocuteurs, pas avec la taille du code |
| Gestion de projet | % de la charge de réalisation | Croît en appel d'offres, en multi-partie prenante, en projet long |
| Recette et qualification | % de la charge de réalisation | Ne jamais la comprimer : c'est le poste le plus souvent sacrifié et le plus souvent regretté |
| Mise en production / DevOps | Forfait par environnement | Multiplier par le nombre d'environnements réellement demandés |
| Documentation et formation | Forfait | Obligatoire dès qu'il y a un back-office ou une reprise par une autre équipe |
| Garantie | % du total, ou forfait sur une période | Vérifier la durée attendue par le client ; en AO, elle est souvent imposée |
| Aléas | % du total | Se justifie par l'incertitude réelle : nombre de fonctions `À confirmer`, dépendances externes, maturité du besoin |

**Ne pas empiler les pourcentages sans les expliciter.** Un chiffrage où le transverse dépasse la réalisation sans justification ne passera pas une revue interne — et un chiffrage où il est absent ne tiendra pas en exécution.

## 4. Les pièges

- **Chiffrer l'interface sans l'intégration** — la couverture liste les deux, le chiffrage doit les porter toutes les deux.
- **Oublier l'administration** — le back-office qui pilote une fonction client coûte souvent autant qu'elle.
- **Traiter les fonctions déduites comme acquises** — elles doivent rester dans un sous-total distinct jusqu'à validation du client.
- **Lisser les incertitudes** — un chiffre rond et unique sur une fonction mal définie donne une fausse impression de maîtrise. Mieux vaut une charge assortie d'une hypothèse écrite.
- **Raboter pour atteindre une cible budgétaire** — si le total dépasse la contrainte annoncée, le dire et proposer des arbitrages de périmètre. Ajuster les charges en silence déplace le problème vers l'exécution.
- **Chiffrer un périmètre absent de la couverture** — si une fonction manque, c'est la couverture qu'il faut reprendre.

## 5. La présentation

- Une ligne du chiffrage = une ligne de la couverture, même référence. C'est ce qui permet de discuter un budget sans le refaire.
- Trois nombres en tête : socle engagé, sous réserve de validation, total.
- Les charges en jours par pas de 0,5 ; les montants en euros entiers.
- Toute hypothèse de calibrage, tout taux de confiance faible, tout profil manquant se retrouve dans « Hypothèses et points de vigilance ». Un chiffrage dont on ne voit pas les hypothèses ne peut pas être challengé.
