# 🎵 Agent Musical Azure OpenAI

Agent intelligent utilisant Azure OpenAI et LangChain pour adapter des partitions musicales à différentes gammes de notes.

## 📋 Prérequis

- Python 3.8 ou supérieur
- Un compte Azure avec une ressource Azure OpenAI déployée
- Un modèle GPT-4o (ou GPT-4) déployé sur Azure

## 🚀 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configurer Azure OpenAI

#### a) Créer une ressource Azure OpenAI

1. Connectez-vous au [portail Azure](https://portal.azure.com)
2. Recherchez "Azure OpenAI" dans la barre de recherche
3. Cliquez sur "Créer" et remplissez les informations requises
4. Une fois créée, allez dans la ressource

#### b) Déployer un modèle

1. Dans votre ressource Azure OpenAI, allez dans "Déploiements" (ou "Deployments")
2. Cliquez sur "Créer un déploiement"
3. Choisissez le modèle **gpt-4o** (recommandé) ou gpt-4
4. Donnez un nom au déploiement (ex: `gpt-4o`)
5. Notez ce nom de déploiement

#### c) Récupérer vos credentials

1. Dans votre ressource Azure OpenAI, allez dans "Clés et point de terminaison" (ou "Keys and Endpoint")
2. Copiez :
   - **Point de terminaison** (Endpoint) : ressemble à `https://votre-resource.openai.azure.com/`
   - **Clé** (Key 1 ou Key 2) : une longue chaîne de caractères

### 3. Configurer les variables d'environnement

1. Copiez le fichier `.env.example` vers `.env` :
   ```bash
   cp .env.example .env
   ```

2. Ouvrez le fichier `.env` et remplissez avec vos informations Azure :
   ```bash
   AZURE_OPENAI_ENDPOINT=https://votre-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=votre_cle_api_ici
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   ```

   **IMPORTANT** : 
   - L'endpoint doit se terminer par `/`
   - Le deployment name doit correspondre au nom que vous avez donné lors du déploiement
   - Ne committez JAMAIS le fichier `.env` dans git (il est déjà dans .gitignore)

## ⚙️ Configuration des gammes

Les gammes musicales sont configurées dans le fichier `config.yaml`. Vous pouvez :

- Ajouter de nouvelles gammes
- Modifier les notes existantes
- Changer les descriptions

Exemple de structure :
```yaml
gammes:
  do_majeur:
    notes: [C, D, E, F, G, A, B]
    description: "Gamme de Do majeur (C major)"
```

## 🎮 Utilisation

### Lancer l'application

```bash
python main.py
```

### Commandes disponibles

- `/help` - Affiche l'aide
- `/gammes` - Liste les gammes configurées
- `/clear` - Efface l'historique de conversation
- `/history` - Affiche l'historique
- `/quit` - Quitte l'application

### Exemples de questions

1. **Lister les gammes** :
   ```
   Quelles gammes sont disponibles ?
   ```

2. **Transposer une mélodie** :
   ```
   Transpose cette mélodie C, D, E, F, G vers la gamme de sol majeur
   ```

3. **Adapter une partition** :
   ```
   Adapte la partition C, E, G, B, D vers re_mineur
   ```

4. **Vérifier une note** :
   ```
   Est-ce que la note F# est dans la gamme de do majeur ?
   ```

5. **Analyse complexe** :
   ```
   Voici une mélodie: A B C# D E. Transpose-la vers la_mineur et explique les changements
   ```

## 🏗️ Architecture

### Structure du projet

```
.
├── main.py              # Point d'entrée de l'application console
├── agent.py             # Logique de l'agent LangChain
├── music_tools.py       # Outils de manipulation musicale
├── config.yaml          # Configuration des gammes et paramètres
├── .env                 # Variables d'environnement (à créer)
├── .env.example         # Template pour .env
├── requirements.txt     # Dépendances Python
└── README.md           # Cette documentation
```

### Composants principaux

1. **MusicAgent** (`agent.py`)
   - Gère l'interaction avec Azure OpenAI
   - Coordonne les outils musicaux
   - Maintient la mémoire conversationnelle

2. **MusicTools** (`music_tools.py`)
   - Normalisation des notes
   - Vérification des notes dans les gammes
   - Transposition de mélodies
   - Calcul des notes les plus proches

3. **Application Console** (`main.py`)
   - Interface utilisateur
   - Gestion des commandes
   - Affichage formaté avec couleurs

## 🎯 Fonctionnalités

### Capacités de l'agent

- ✅ Lister les gammes disponibles
- ✅ Vérifier si une note est dans une gamme
- ✅ Transposer des mélodies vers différentes gammes
- ✅ Extraire des notes depuis du texte
- ✅ Trouver les notes les plus proches
- ✅ Expliquer les transpositions effectuées
- ✅ Maintenir le contexte conversationnel

### Formats supportés

L'agent peut comprendre les notes au format :
- Notation anglo-saxonne : C, D, E, F, G, A, B
- Altérations : C#, Db, F#, Bb
- Symboles Unicode : ♯, ♭

## 🔧 Personnalisation

### Ajouter une gamme

Éditez `config.yaml` :
```yaml
gammes:
  ma_nouvelle_gamme:
    notes: [C, D, E, F#, G, A, B]
    description: "Ma gamme personnalisée"
```

### Modifier le comportement de l'agent

Dans `config.yaml`, section `agent` :
- `temperature` : 0.0 (déterministe) à 1.0 (créatif)
- `max_tokens` : Longueur maximale des réponses
- `system_prompt` : Instructions système pour l'agent

### Configurer la mémoire

Dans `config.yaml`, section `memory` :
- `type` : "buffer" (garde les N derniers messages) ou "none"
- `max_messages` : Nombre de messages à conserver

## 🐛 Dépannage

### Erreur : "Variables d'environnement manquantes"

➡️ Vérifiez que le fichier `.env` existe et contient toutes les variables requises

### Erreur : "Model not found"

➡️ Vérifiez que `AZURE_OPENAI_DEPLOYMENT_NAME` correspond au nom exact de votre déploiement

### Erreur : "Invalid API key"

➡️ Vérifiez que votre clé API est correcte et que votre ressource Azure est active

### L'agent ne trouve pas les gammes

➡️ Vérifiez la syntaxe de `config.yaml` (indentation YAML stricte)

## 📚 Ressources

- [Documentation Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Documentation LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Théorie musicale](https://fr.wikipedia.org/wiki/Gamme_musicale)

## 📝 Licence

Ce projet est fourni à titre d'exemple. Adaptez-le selon vos besoins.

## 🤝 Support

Pour toute question ou problème :
1. Vérifiez d'abord ce README
2. Consultez les logs d'erreur détaillés
3. Vérifiez votre configuration Azure

---

**Bon développement ! 🎵**
