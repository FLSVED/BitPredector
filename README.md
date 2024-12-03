BitPredector est une application web innovante conçue pour analyser et prédire les tendances des prix des crypto-monnaies en exploitant l'analyse de sentiment et l'agrégation de données issues des réseaux sociaux et des actualités. Ce projet est en phase de développement initial et vise à offrir des insights fiables pour les traders et les investisseurs.

## Table des Matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Architecture du Projet](#architecture-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Roadmap](#roadmap)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Contact](#contact)

## Description

BitPredector est une application web en développement qui vise à fournir des prédictions sur les tendances des crypto-monnaies. En utilisant des techniques avancées d'analyse de données, l'application collecte et analyse les informations provenant des réseaux sociaux pour aider les utilisateurs à prendre des décisions éclairées.

## Fonctionnalités

- **Analyse de Sentiment** : Évalue les sentiments des utilisateurs sur les plateformes de réseaux sociaux.
- **Agrégation de Données** : Récupère et analyse les actualités pour identifier les tendances émergentes.
- **Prédictions Précoces** : Utilise des modèles de machine learning pour prédire les mouvements des prix des crypto-monnaies.
- **Interface Utilisateur Moderne** : Interface basée sur React pour une expérience utilisateur fluide et interactive.

## Architecture du Projet

Le projet est structuré comme suit :

```
/bitpredector
|-- /backend
|   |-- /data_sources
|   |-- /models
|   |-- /tests
|-- /frontend
|   |-- /src
|   |-- /public
```

## Prérequis

- **Python 3.9+**
- **Node.js 16+**
- **npm 7+**
- **Git**

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/FLSVED/bitpredector.git
   cd bitpredector
   ```

2. Installez les dépendances du backend :

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Installez les dépendances du frontend :

   ```bash
   cd ../frontend
   npm install
   ```

## Utilisation

1. Lancez le backend :

   ```bash
   cd backend
   source venv/bin/activate
   python run.py
   ```

2. Lancez le frontend :

   ```bash
   cd ../frontend
   npm start
   ```

3. Ouvrez votre navigateur à `http://localhost:3000` pour utiliser l'application.

## Roadmap

- [ ] Implémenter l'analyse de sentiment basique
- [ ] Intégrer l'agrégation de données d'actualités
- [ ] Développer le module de prédiction initial
- [ ] Créer un tableau de bord interactif pour l'affichage des données
- [ ] Publier une première version bêta

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/NouvelleFonctionnalité`).
3. Commitez vos modifications (`git commit -m 'Description de la fonctionnalité'`).
4. Poussez la branche (`git push origin feature/NouvelleFonctionnalité`).
5. Ouvrez une Pull Request.

Assurez-vous de respecter le style de code du projet et d'ajouter des tests pour toute nouvelle fonctionnalité.

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
