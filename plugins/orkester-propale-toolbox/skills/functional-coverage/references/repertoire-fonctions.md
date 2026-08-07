# Répertoire des fonctions récurrentes

Ce répertoire recense les fonctions qui reviennent d'un projet Orkester à l'autre. Il sert à **challenger une couverture déjà établie depuis les sources** — jamais à la générer. Une fonction ne s'ajoute que si le projet la justifie réellement ; une liste complète mais générique vaut moins qu'une liste courte et juste.

Chaque domaine porte une **condition de pertinence** : quand le domaine mérite d'être passé en revue. Les noms proposés sont des formulations types à adapter au vocabulaire du projet.

---

## A. Compte et accès

*Pertinent dès qu'il existe un utilisateur identifié — donc presque toujours, sur chaque brique applicative.*

- Authentification
- Création de compte / inscription
- Mot de passe oublié
- Double authentification (2FA)
- SSO / connexion déléguée
- Gestion du profil utilisateur
- Gestion des rôles et droits
- Gestion des utilisateurs (administration)
- Invitation d'un collaborateur
- Multi-comptes / changement d'entité

> L'authentification apparaît sur **chaque** brique applicative (portail, back-office, mobile) : ce sont des charges distinctes.

## B. Espace client et pilotage

*Pertinent dès qu'un utilisateur dispose d'un espace personnel ou professionnel.*

- Dashboard client
- Dashboard statistiques
- Historique d'activité
- Notifications in-app
- Centre d'aide / FAQ
- Recherche globale
- Préférences et paramétrage

## C. Données et référentiels

*Pertinent dès que la solution manipule des objets métier structurés.*

- Gestion des données clients
- Gestion des {objets métier du projet}
- Import de données (fichier, masse)
- Export de données
- Référentiels et nomenclatures
- Historisation / journal des modifications
- Contrôles et règles de cohérence
- Déduplication

> Le nom doit reprendre l'objet métier réel du projet (« Gestion des données des biens immobiliers », « Gestion plan d'amortissement »), pas un terme générique.

## D. Catalogue et recherche

*Pertinent en `ECOM_B2B` / `ECOM_B2C`, ou dès qu'il existe une offre à parcourir.*

- Gestion du catalogue produits
- Fiche produit
- Recherche et moteur de recherche
- Filtres et navigation à facettes
- Gestion des stocks
- Tarification et grilles de prix
- Tarifs négociés / spécifiques client
- Promotions et remises
- Gestion des médias produits

## E. Commande et tunnel d'achat

*Pertinent dès qu'il y a une transaction ou une souscription.*

- Panier
- Tunnel d'achat
- Prise de commande
- Devis
- Validation / workflow d'approbation
- Suivi de commande
- Retours et annulations
- Réachat / commande récurrente
- Listes d'achat / favoris

## F. Paiement, facturation, comptabilité

*Pertinent dès qu'il y a un flux financier. Le service de paiement forme sa propre brique.*

- Paiement CB
- Paiement SEPA / prélèvement
- Paiement à échéance / encours
- Abonnement et récurrence
- Génération de facture
- Avoirs et remboursements
- Relances et impayés
- Export comptable (FEC, liasse)
- Paramétrage du plan comptable
- Contrôles fiscaux

## G. Logistique et livraison

*Pertinent en e-commerce physique ou dès qu'un bien circule.*

- Gestion des adresses de livraison
- Choix du mode de livraison
- Calcul des frais de port
- Suivi de colis
- Gestion des transporteurs
- Points relais
- Bons de préparation / expédition

## H. Back-office et administration

*Pertinent dès qu'un opérateur interne intervient. Le domaine le plus souvent sous-estimé par les cahiers des charges.*

- Dashboard admin
- Gestion des dossiers clients
- Gestion des clients / comptes
- Gestion des utilisateurs back-office
- Paramétrage fonctionnel
- Modération / validation
- Support et prise de main
- Exports et rapports
- Journal d'administration

## I. Documents et médias

*Pertinent dès que la solution produit, stocke ou échange des fichiers.*

- Dépôt de document
- Stockage de médias et documents
- Génération de document (PDF)
- Signature électronique
- Partage de document
- Téléchargement de dossier / archive
- Archivage et durée de conservation
- Scan mobile / capture

## J. Notifications et emailing

*Pertinent dès qu'il y a communication sortante. Le service d'emailing forme sa propre brique.*

- Gestion des templates email
- Envoi des emails transactionnels
- Notifications push
- SMS
- Préférences de communication
- Campagnes / envois groupés

## K. IA et automatisation

*Pertinent quand les sources mentionnent de l'IA, de l'OCR, de la reconnaissance ou de l'assistance automatisée. Le modèle utilisé forme sa propre brique.*

- OCR / lecture de document
- Extraction de données structurées
- Contrôles de cohérence automatiques
- Suggestions et recommandations
- Assistant conversationnel
- Détection d'anomalies
- Classification automatique

> Distinguer systématiquement la fonction côté interface (ce que l'utilisateur voit) et l'intégration côté service (le prompt, l'appel, le post-traitement, les garde-fous) : deux charges.

## L. Intégrations et services tiers

*Pertinent dès qu'un système externe est nommé. Un groupe par service ; y lister ce que l'intégration doit couvrir.*

- Synchronisation {objet} avec {système}
- Remontée / descente de flux
- Authentification et gestion des jetons
- Gestion des erreurs et rejeux
- Webhooks
- Mapping et transcodification
- Supervision des flux

> Services fréquents : ERP, CRM, PIM, OMS, WMS, comptabilité, paiement, emailing, identité, transporteur, service d'adresses, référentiels publics (SIRET, INPI, INSEE).

## M. Spécifique mobile

*Pertinent en `APP_MOBILE`.*

- Onboarding
- Mode hors ligne
- Synchronisation
- Notifications push
- Accès appareil photo / scan
- Géolocalisation
- Biométrie
- Publication sur les stores
- Mise à jour forcée

## N. Conformité et sécurité

*Pertinent en `APPEL_OFFRES`, `ECOM_B2B`, grand compte, secteur réglementé, ou données sensibles.*

- Gestion du consentement / cookies
- Export et suppression des données personnelles
- Journalisation et traçabilité
- Gestion des habilitations fines
- Chiffrement et cloisonnement
- Accessibilité (RGAA / WCAG)
- Mentions légales et CGV/CGU

## O. Exploitation et RUN

*Pertinent en `RUN` (TMA / TME / reprise), ou pour le volet maintenance d'un `BUILD`.*

- Reprise de l'existant
- Migration de données
- Supervision et alerting
- Sauvegarde et restauration
- Gestion des environnements
- Déploiement et livraison
- Gestion des demandes / tickets
- Correctifs et maintenance évolutive
- Réversibilité

---

## Les oublis les plus coûteux

Passer explicitement ces six points en revue avant de figer la couverture — ce sont ceux qui manquent le plus souvent aux cahiers des charges et qui pèsent le plus au chiffrage :

1. **L'administration** — qui gère les utilisateurs, les droits, le paramétrage ? Un back-office est presque toujours nécessaire, rarement demandé.
2. **La reprise de données** — que devient l'existant ? Le volume et la qualité des données à reprendre pèsent souvent plus que plusieurs fonctions.
3. **Les exports** — comptabilité, reporting, obligations légales : presque toujours attendus, presque jamais écrits.
4. **La gestion des erreurs des services tiers** — rejeux, réconciliation, alertes : la moitié de la charge d'une intégration.
5. **Les états intermédiaires** — brouillons, validations, annulations, reprises de saisie : invisibles dans un cahier des charges, structurants dans l'implémentation.
6. **Le multi-{quelque chose}** — multi-entité, multi-langue, multi-devise, multi-site : à confirmer explicitement, jamais à supposer.
