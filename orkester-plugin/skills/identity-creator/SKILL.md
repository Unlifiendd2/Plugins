---
name: identity-creator
description: >-
  Rédige les sections « identité » d'une proposition commerciale (propale) Orkester — le bloc B :
  qui sommes-nous, proposition de valeur / ADN, domaines d'intervention, expertises &
  certifications, pourquoi Orkester, historique de la relation, références clients. Prend en
  entrée une trame, la position de la ou des sections dans le plan, et le contexte projet, puis
  produit un contenu rédigé prêt à intégrer, en s'appuyant en priorité sur la base Orkester-kb
  (propales gagnantes) et en l'adaptant finement au client. À déclencher depuis le skill
  propale-maker, ou dès que l'utilisateur veut rédiger, produire ou améliorer une section de
  présentation, de légitimité, de positionnement ou de références d'une propale Orkester — même
  s'il ne nomme pas explicitement le « bloc B » ou la « section identité ».
---

# Rédaction des sections identité (bloc B) — propale Orkester

Tu t'adresses à un project owner expérimenté de Orkester. N'aie pas peur du jargon métier (build/run, TMA/TME, BFF, MVP, comitologie, SLA…) ; ne le vulgarise pas sauf demande explicite.

## Ce que fait ce skill

Le **bloc B** d'une proposition commerciale (propale) Orkester établit *qui est Orkester et pourquoi le client devrait lui faire confiance*. C'est le moment où le document quitte le monde du client pour parler de l'agence — le risque est double : sonner générique (un « qui sommes-nous » interchangeable) ou se couper du fil rouge centré client. Ce skill rédige ces sections de façon **spécifique, crédible et au service du récit**.

Orkester capitalise sur ses propales gagnantes : les faits d'identité (effectifs, implantations Paris-Laval, chiffres, partenariats, certifications, références) y sont déjà formulés. Le rôle du skill n'est pas de réinventer ces contenus mais de **les retrouver dans `Orkester-kb`, les vérifier, puis les recontextualiser** pour CE client et CETTE position dans le plan.

Sections couvertes : **B1** (qui sommes-nous), **B2** (proposition de valeur / ADN), **B3** (domaines d'intervention), **B4** (expertises : technos, partenariats, certifications), **B5** (pourquoi Orkester pour ce projet), **B6** (historique / rétrospective de la relation), **B7** (références emblématiques).

## Les trois entrées

Avant de rédiger, réunir ces trois éléments. S'il en manque un, renvoyer un message final en expliquant ce qu'il manque.

1. **La trame** — le plan. On y lit, pour chaque section identité, son **statut** et surtout ses consignes **« À rédiger »** : ce sont des instructions fermes, pas des suggestions. Si la trame définit un **fil rouge / promesse-signature**, il prime sur tout : chaque section identité doit le servir.
2. **La position de la section dans le plan** — l'ordre détermine ce que la section doit *préparer* (ce qui suit) et *encaisser* (ce qui précède). Une section identité placée tôt n'a pas le même travail que la même placée après la compréhension du besoin. Voir « Lire la position » plus bas.
3. **Le contexte projet** — au minimum les 4 axes de qualification (BUILD/RUN ; ECOM_B2B / ECOM_B2C / APP_MOBILE ; NOUVEAU_CLIENT / CLIENT_EXISTANT ; APPEL_OFFRES / ECHANGE_DIRECT), le nom et le secteur du client, et tout élément différenciant connu. Les axes pilotent le filtrage du contenu (cf. référence).

## Principe de sourcing : hybride, KB d'abord, jamais inventer

Les sections identité contiennent des **faits sur Orkester** : chiffres, dates, noms de clients, certifications, partenariats technologiques. Ces faits ne s'inventent pas — un chiffre faux ou une référence client fantôme dans une propale est une faute grave, surtout en appel d'offres où le client vérifie.

Procéder ainsi :

1. **Interroger `Orkester-kb` en premier.** Utiliser `search_kb_semantic` ou `search_kb_hybrid` pour retrouver comment Orkester a rédigé cette section dans des propales gagnantes comparables (filtrer mentalement par les 4 axes : un « pourquoi Orkester » d'une TMA B2B existante n'est pas celui d'un build B2C en prospect). Utiliser `get_full_document` sur une source `propale_*.md` proche pour récupérer la formulation canonique complète, et `get_adjacent_chunks` pour le contexte autour d'un passage.
2. **Extraire les faits réutilisables** (chiffres, implantations, partenariats, certifs, références) et **les phrases de positionnement** qui ont fait leurs preuves.
3. **Recontextualiser** au client courant : reformuler pour parler de SON secteur, SON enjeu, SON projet. Le fond factuel vient de la KB ; l'angle vient du contexte projet.
4. **Repli sur le contexte projet** seulement là où la KB est muette. Tout fait non confirmé par la KB ni fourni par l'utilisateur doit apparaître comme un **placeholder explicite** — p. ex. `[À CONFIRMER : effectif support 24x7]` — jamais comme une affirmation. Signaler ces placeholders en fin de livrable.

En résumé : la KB est la source de vérité des faits ; le contexte projet est la source de l'angle ; l'invention n'est jamais une source.

## Workflow

1. **Cadrer.** Identifier la/les section(s) B demandée(s), lire leurs consignes « À rédiger » dans la trame, repérer le fil rouge et les 4 axes.
2. **Lire la référence.** Ouvrir `references/bloc-B-identite.md` et lire **uniquement** les entrées des sections demandées : objectif, ce qu'il faut chercher dans la KB, leviers de contextualisation, pièges.
3. **Sourcer.** Interroger `Orkester-kb` (cf. principe ci-dessus) pour chaque section. Si l'utilisateur a fourni une fiche d'identité / un brief, le croiser avec la KB.
4. **Lire la position.** Pour chaque section, noter ce qu'elle suit et précède, et ajuster (cf. « Lire la position »).
5. **Rédiger.** Produire la prose au format de sortie, en respectant la langue de la propale, la voix Orkester, les consignes de la trame et le fil rouge.
6. **Contrôler.** Relire : aucun fait inventé, placeholders signalés, pas de redite avec les sections voisines, le fil rouge est servi.

## Lire la position dans le plan

L'ordre raconte une histoire ; la section doit y trouver sa place sans répéter ni contredire ses voisines.

- **Ce qui précède** = ce qui est déjà acquis. Ne pas re-présenter Orkester si B1 l'a déjà fait ; ne pas re-justifier le positionnement si B2 l'a posé. Enchaîner, ne pas boucler.
- **Ce qui suit** = ce que la section doit préparer. Une B2 (ADN) placée juste avant la réponse technique doit amorcer les partis-pris qui seront développés ; une B7 (références) placée juste avant la réponse au besoin doit installer la preuve qui rend crédible la suite.
- **Position précoce** (avant la compréhension du besoin, cas `CLIENT_EXISTANT` où B5/B6 ouvrent) → capitaliser d'emblée sur la relation, ton de continuité.
- **Position tardive / réassurance** → ton de consolidation, on confirme une confiance déjà installée.
- **Si la trame nomme un fil rouge**, chaque section B doit le faire avancer : l'amorcer (sections d'ouverture), l'incarner (B5 surtout), ou le rappeler (sections tardives).

## Voix et langue

- **Langue** : rédiger dans la langue de la propale, déduite du contexte projet (p. ex. client US → anglais ; soigner alors le vocabulaire métier dans cette langue).
- **Voix Orkester** : assurée sans arrogance, concrète, orientée valeur client. « Nous venons du build et ça change tout » est un marqueur ADN, pas un slogan creux — l'étayer.
- **Spécificité** : bannir le générique. Chaque paragraphe doit pouvoir être attribué à CE client. Si une phrase fonctionnerait à l'identique pour n'importe quel prospect, la réécrire.

## Format de sortie

Pour chaque section demandée :

```
## [Code] Titre de la section
<prose rédigée, prête à intégrer — paragraphes ; tableau seulement si la section l'exige (B3/B4)>

> Notes de rédaction
> - Sources KB : <documents propale_* mobilisés, le cas échéant>
> - À confirmer : <placeholders / faits à vérifier — ou « aucun »>
> - Lien au fil rouge : <comment la section sert la promesse-signature>
```

Rendre le contenu directement réutilisable : pas de méta-commentaire dans la prose elle-même, tout le commentaire va dans les « Notes de rédaction ».

## Pièges à éviter

- **Le « qui sommes-nous » générique** : le piège n°1. Filtrer B3/B4 sur ce qui sert le deal, couper le reste.
- **Inventer des références ou des chiffres** : interdit. KB ou placeholder.
- **B6 hors `CLIENT_EXISTANT`** : ne pas rédiger d'historique de relation pour un prospect ; le signaler si demandé à tort.
- **Redondance avec les voisines** : B1↔B2↔B5 se chevauchent facilement (présentation / positionnement / pourquoi nous). Donner à chacune un travail distinct (cf. référence).
- **Ignorer le fil rouge** : une section identité techniquement juste mais déconnectée du récit affaiblit la propale.

Pour le détail par section (objectif, recherche KB, leviers, pièges propres), lire `references/bloc-B-identite.md`.