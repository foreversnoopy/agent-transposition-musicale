# Instructions Copilot - Agent Musical Azure OpenAI

## 🎯 Vue d'ensemble du projet

Ce projet est un **agent intelligent de transposition musicale** utilisant Azure OpenAI et LangChain. L'agent permet d'adapter des partitions musicales à différentes gammes de notes prédéfinies.

## 🏗️ Architecture

### Composants principaux

1. **`main.py`** - Application console interactive
   - Interface utilisateur avec colorama
   - Gestion des commandes système (/help, /quit, /clear, etc.)
   - Boucle d'interaction utilisateur

2. **`agent.py`** - Cœur de l'agent LangChain
   - Initialisation du client Azure OpenAI avec `AzureChatOpenAI`
   - Gestion de la mémoire conversationnelle (`ConversationBufferMemory`)
   - Création et orchestration des outils (functions) pour l'agent
   - Utilise `create_openai_functions_agent` et `AgentExecutor`

3. **`music_tools.py`** - Logique musicale pure
   - Manipulation et normalisation des notes musicales
   - Calculs de transposition entre gammes
   - Algorithmes de recherche de notes les plus proches
   - Gestion des équivalents enharmoniques (C#/Db, etc.)

4. **`config.yaml`** - Configuration centralisée
   - Définition des gammes de notes disponibles
   - Paramètres de l'agent (temperature, max_tokens)
   - System prompt avec les règles strictes de l'agent
   - Configuration de la mémoire

## 🔑 Concepts clés

### Gammes musicales
- Chaque gamme est définie par un nom unique et une liste de notes
- Format: `[C, D, E, F, G, A, B]` (notation anglo-saxonne)
- Support des altérations: `#` (dièse) et `b` (bémol)
- Les gammes sont facilement extensibles via `config.yaml`

### Outils (Functions) de l'agent
L'agent dispose de 4 outils LangChain:

1. **`list_available_scales`** - Liste toutes les gammes configurées
2. **`check_note_in_scale`** - Vérifie si une note appartient à une gamme
3. **`transpose_melody_to_scale`** - Transpose une série de notes vers une gamme cible
4. **`extract_notes_from_text`** - Parse et extrait les notes d'un texte libre

### Algorithme de transposition
1. Pour chaque note de la mélodie source:
   - Si la note est dans la gamme cible → la conserver
   - Sinon → trouver la note la plus proche dans la gamme cible
2. La distance est calculée en demi-tons (échelle chromatique)
3. Les équivalents enharmoniques sont gérés (C# = Db)

## 📝 Conventions de code

### Style Python
- **PEP 8** pour le formatage
- Docstrings pour toutes les classes et méthodes publiques
- Type hints pour les signatures de fonctions
- Commentaires explicatifs pour la logique complexe

### Gestion des erreurs
- Try-except avec messages d'erreur clairs pour l'utilisateur
- Validation des entrées utilisateur
- Gestion gracieuse des erreurs API Azure

### Configuration
- Variables sensibles dans `.env` (jamais commitées)
- Configuration métier dans `config.yaml`
- Séparation claire entre config et code

## 🔧 Modifications courantes

### Ajouter une nouvelle gamme

**Fichier**: `config.yaml`

```yaml
gammes:
  nouvelle_gamme:
    notes: [C, D, E, F#, G, A, Bb]
    description: "Description de la gamme"
```

### Ajouter un nouvel outil pour l'agent

**Fichier**: `agent.py`, méthode `_create_tools()`

```python
def nouveau_tool(param: str) -> str:
    """Description de l'outil"""
    # Logique de l'outil
    return result

tools.append(StructuredTool.from_function(
    func=nouveau_tool,
    name="nom_outil",
    description="Description détaillée pour que l'agent sache quand l'utiliser"
))
```

### Modifier le comportement de l'agent

**Fichier**: `config.yaml`, section `agent.system_prompt`

Ajustez les instructions système pour modifier:
- Les règles de transposition
- Le style de réponse
- Les contraintes à respecter

### Changer le modèle Azure OpenAI

**Fichier**: `.env`

```bash
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4  # ou gpt-35-turbo, etc.
```

Ajustez aussi `temperature` dans `config.yaml` selon le modèle.

## 🐛 Debugging

### Logs verbeux
L'agent utilise `verbose=True` dans `AgentExecutor` - les étapes intermédiaires sont affichées.

### Tester les outils individuellement
```python
from music_tools import MusicTools
from config import load_config

config = load_config()
tools = MusicTools(config['gammes'])
result = tools.transpose_melody(['C', 'D', 'E'], 'sol_majeur')
print(result)
```

### Problèmes courants

1. **"Model not found"** → Vérifier `AZURE_OPENAI_DEPLOYMENT_NAME`
2. **"Invalid API key"** → Vérifier `AZURE_OPENAI_API_KEY` dans `.env`
3. **Gamme non trouvée** → Vérifier l'orthographe exacte dans `config.yaml`
4. **Parsing YAML échoue** → Vérifier l'indentation (espaces, pas de tabs)

## 🚀 Extensions possibles

### Fonctionnalités musicales avancées
- Support des accords (triades, septièmes)
- Reconnaissance de progressions harmoniques
- Suggestions de réharmonisation
- Support de formats de partition (MusicXML, MIDI)

### Améliorations techniques
- Streaming des réponses pour de meilleures performances
- Cache des transpositions fréquentes
- Support multi-utilisateurs avec sessions
- API REST pour intégration web
- Tests unitaires et d'intégration

### Interface utilisateur
- Interface graphique (Gradio, Streamlit)
- Application web (FastAPI + React)
- Export PDF des partitions transposées
- Lecture audio des mélodies

## 🔐 Sécurité

### Bonnes pratiques
- ✅ `.env` est dans `.gitignore`
- ✅ Pas de credentials en dur dans le code
- ✅ Validation des entrées utilisateur
- ⚠️ Pour la production: utiliser Azure Key Vault pour les secrets

### Limites de rate
Azure OpenAI a des limites de requêtes:
- Surveiller les quotas dans le portail Azure
- Implémenter du retry avec backoff exponentiel si nécessaire

## 📚 Ressources

### Documentation
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [LangChain Python](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

### Théorie musicale
- [Gammes musicales](https://fr.wikipedia.org/wiki/Gamme_musicale)
- [Transposition musicale](https://fr.wikipedia.org/wiki/Transposition_(musique))
- [Notes enharmoniques](https://fr.wikipedia.org/wiki/Enharmonie)

## 💡 Conseils pour Copilot

Quand tu travailles sur ce projet:

1. **Respecte la séparation des responsabilités**:
   - Logique musicale → `music_tools.py`
   - Logique agent → `agent.py`
   - Interface → `main.py`

2. **Maintiens la cohérence**:
   - Les gammes DOIVENT être définies dans `config.yaml`
   - Les credentials DOIVENT être dans `.env`
   - Le system prompt définit le comportement global

3. **Privilégie la clarté**:
   - Code lisible > code clever
   - Commentaires pour la logique musicale complexe
   - Messages d'erreur explicites pour l'utilisateur

4. **Teste les modifications**:
   - Vérifie que l'agent peut toujours lister les gammes
   - Teste une transposition simple après chaque changement
   - Vérifie que la mémoire conversationnelle fonctionne

5. **Pense à l'utilisateur final**:
   - Messages colorés et formatés dans la console
   - Instructions claires dans le README
   - Aide contextuelle avec `/help`

## 🎼 Philosophie du projet

Cet agent est conçu pour être:
- **Contraint**: Il utilise UNIQUEMENT les gammes configurées (pas d'hallucination)
- **Explicatif**: Il explique chaque transposition effectuée
- **Extensible**: Facile d'ajouter de nouvelles gammes ou fonctionnalités
- **Professionnel**: Architecture propre, séparation des concerns, documentation

L'objectif n'est pas de créer un outil parfait de théorie musicale, mais un **exemple robuste** d'agent Azure OpenAI avec contraintes métier strictes et outils personnalisés.
