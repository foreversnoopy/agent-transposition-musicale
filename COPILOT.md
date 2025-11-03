# GitHub Copilot Chat — Recommandations pour ce projet

Ce fichier donne des recommandations sur le choix du modèle Copilot Chat et propose des templates de prompt pour utiliser Copilot efficacement dans le workspace `agent-transposition-musicale`.

## Modèles recommandés

- GPT-4.1 — Recommandation par défaut pour les tâches critiques (design, refactor, génération de tests). Précis et fiable.
- GPT-4o — Bon compromis vitesse/qualité pour développement quotidien.
- Grok Code Fast 1 — Ultra-rapide pour complétions courtes, recherche de patterns et navigation dans le code.
- GPT-5 mini — À utiliser pour expérimentations et approches alternatives (moins éprouvé pour code productif).

## Quand utiliser quoi

- Utilise `GPT-4.1` pour:
  - Conception d'API, refactors importants, revues de PR, génération détaillée de tests unitaires.
  - Expliquer les décisions, produire des patchs complexes.

- Utilise `GPT-4o` pour:
  - Développement quotidien, complétions de fonctions, génération rapide de tests.

- Utilise `Grok Code Fast 1` pour:
  - Recherche de code, complétions courtes, explorer rapidement le repo.

- Utilise `GPT-5 mini` pour:
  - Expérimentations et idées alternatives.

## Templates de prompt pour Copilot Chat

1) Refactor + tests (utiliser GPT-4.1)

```
Contexte: Projet 'agent-transposition-musicale'. Fichier: {path}
Tâche: Refactoriser la fonction {function_name} pour améliorer la lisibilité et la testabilité.
Contraintes:
- Ne change pas l'API publique (signatures des fonctions).
- Ajoute/actualise des tests pytest couvrant les cas normaux et bords.
Livrables attendus:
- Patch diff (format git) appliquant les changements.
- Un fichier de tests `tests/test_{module}.py` avec au moins 3 cas.
- Une brève explication (3 à 5 lignes) décrivant les changements et risques.
```

2) Ajouter support d'un LLM local (ex: LlamaCpp) dans `agent.py` (utiliser GPT-4.1 ou GPT-4o)

```
Contexte: Le projet doit pouvoir utiliser AzureChatOpenAI ou un LLM local via LlamaCpp.
Tâche: Générer un patch pour:
- Ajouter une fonction `get_llm(config)` qui retourne soit AzureChatOpenAI soit LlamaCpp selon `config['local_llm']`.
- Minimiser les changements en réutilisant le code existant.
- Ajouter un petit test unitaire qui vérifie le type retourné pour `local_llm: true/false`.
Livrables: patch + tests + instructions d'installation minimal (pip requirements).
```

3) Requête rapide pour navigation (Grok Code Fast 1)

```
Contexte: Cherche où `transpose_melody` est appelé dans le repo.
Tâche: Donne la liste des fichiers et les lignes de code où `transpose_melody` est invoquée, puis propose une suggestion courte pour centraliser les validations.
```

## Bonnes pratiques

- Toujours demander à Copilot de générer tests unitaires pour changements non triviaux.
- Pour chaque patch demandée: demander un résumé `What Changed / Why / Risks`.
- Fournir aux prompts les fichiers pertinents (colle le contenu ou la fonction) pour réduire les hallucinations.
- Toujours relire et exécuter les tests localement avant de merger.

---

Si tu veux, je peux committer ce fichier sur une branche `copilot-guidance` et pousser le commit. Veux-tu que je le fasse maintenant ?
