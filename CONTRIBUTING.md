# Guide de Contribution - Lotusette

Merci de votre intérêt pour contribuer à Lotusette ! Ce document vous guidera à travers le processus de contribution.

## 📋 Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Configuration de l'environnement](#configuration-de-lenvironnement)
- [Standards de code](#standards-de-code)
- [Processus de Pull Request](#processus-de-pull-request)
- [Reporting de bugs](#reporting-de-bugs)
- [Propositions de fonctionnalités](#propositions-de-fonctionnalités)

## Code de conduite

Ce projet adhère à un code de conduite. En participant, vous êtes attendu à respecter ce code :

- Soyez respectueux et inclusif
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est mieux pour la communauté
- Faites preuve d'empathie envers les autres membres

## Comment contribuer

### Types de contributions

Nous accueillons plusieurs types de contributions :

1. **Code** : Nouvelles fonctionnalités, corrections de bugs, améliorations
2. **Documentation** : Guides, tutoriels, corrections de typos
3. **Tests** : Nouveaux tests, amélioration de la couverture
4. **Revue de code** : Revue des Pull Requests
5. **Traduction** : Traduction de la documentation
6. **Design** : UI/UX, logos, graphiques
7. **Idées** : Propositions de fonctionnalités, discussions

### Premiers pas

1. **Fork le repository**
2. **Clone votre fork** : `git clone https://github.com/votre-username/Lotusette.git`
3. **Créez une branche** : `git checkout -b feature/ma-fonctionnalite`
4. **Configurez l'environnement** (voir section suivante)

## Configuration de l'environnement

### Prérequis

- Python 3.10 ou supérieur
- Git
- pip ou poetry
- (Optionnel) Docker

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Installer les dépendances de développement
pip install -r requirements-dev.txt

# 4. Installer les pre-commit hooks
pre-commit install

# 5. Copier le fichier d'environnement
cp .env.example .env
# Éditer .env avec vos configurations locales
```

### Configuration des APIs (optionnel pour le développement)

```bash
# Dans .env
OPENAI_API_KEY=your_key_here
# ... autres clés API selon vos besoins
```

### Vérification de l'installation

```bash
# Lancer les tests
pytest

# Lancer les linters
make lint

# Formater le code
make format
```

## Standards de code

### Python

Nous suivons les conventions Python standard avec quelques spécificités :

#### Style

- **PEP 8** pour le style de code
- **Black** pour le formatage (ligne max 100 caractères)
- **isort** pour l'organisation des imports
- **Type hints** requis pour les fonctions publiques

```python
# Bon exemple
def process_message(message: str, user_id: int) -> dict[str, Any]:
    """Process a user message and return a response.
    
    Args:
        message: The user's message text
        user_id: The unique user identifier
        
    Returns:
        A dictionary containing the response and metadata
    """
    # Implementation
    pass
```

#### Naming conventions

- **Fonctions et variables** : `snake_case`
- **Classes** : `PascalCase`
- **Constantes** : `UPPER_SNAKE_CASE`
- **Privé** : `_leading_underscore`

```python
class MessageProcessor:
    """Process user messages."""
    
    MAX_RETRIES = 3
    
    def __init__(self):
        self._cache = {}
    
    def process_message(self, message: str) -> str:
        """Process a message."""
        pass
```

#### Documentation

- **Docstrings** : Google style pour toutes les fonctions/classes publiques
- **Commentaires** : Expliquer le "pourquoi", pas le "quoi"
- **Type hints** : Obligatoire pour APIs publiques

```python
def retrieve_context(
    query: str,
    limit: int = 5,
    threshold: float = 0.7
) -> list[dict[str, Any]]:
    """Retrieve relevant context from memory.
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        threshold: Minimum similarity score (0-1)
        
    Returns:
        List of context dictionaries with 'text' and 'score' keys
        
    Raises:
        MemoryException: If the retrieval fails
    """
    pass
```

### Structure des commits

Format de message de commit :

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types** :
- `feat` : Nouvelle fonctionnalité
- `fix` : Correction de bug
- `docs` : Documentation
- `style` : Formatage, typos
- `refactor` : Refactoring de code
- `test` : Ajout/modification de tests
- `chore` : Maintenance, dependencies

**Exemples** :
```
feat(llm): add Claude provider support

Implement Claude API integration as an alternative LLM provider.
Includes configuration, error handling, and streaming support.

Closes #123
```

```
fix(voice): resolve audio buffer overflow

The audio capture was not properly draining the buffer,
causing memory issues during long sessions.
```

### Tests

- **Coverage minimale** : 80%
- **Tests unitaires** : Pour chaque fonction publique
- **Tests d'intégration** : Pour les flux importants
- **Nommage** : `test_<what>_<condition>_<expected>`

```python
def test_process_message_with_valid_input_returns_response():
    """Test that valid input produces a valid response."""
    processor = MessageProcessor()
    result = processor.process_message("Hello")
    
    assert result["status"] == "success"
    assert "response" in result
    assert len(result["response"]) > 0
```

### Linting et formatage

Avant de soumettre :

```bash
# Formater le code
black .
isort .

# Vérifier le style
flake8
pylint lotusette

# Vérifier les types
mypy lotusette

# Ou utiliser make
make format
make lint
```

## Processus de Pull Request

### Avant de soumettre

1. ✅ Le code suit les standards
2. ✅ Tous les tests passent
3. ✅ La documentation est à jour
4. ✅ Les commits sont bien formatés
5. ✅ Pas de code commenté inutile
6. ✅ Les secrets sont dans .env, pas dans le code

### Soumettre une PR

1. **Push vers votre fork**
   ```bash
   git push origin feature/ma-fonctionnalite
   ```

2. **Créer la Pull Request** sur GitHub

3. **Remplir le template de PR**
   - Description claire des changements
   - Référence aux issues (#123)
   - Screenshots si UI
   - Checklist de vérification

4. **Attendre la revue**
   - Répondre aux commentaires
   - Faire les ajustements demandés
   - Demander une nouvelle revue

### Template de PR

```markdown
## Description
[Décrivez vos changements]

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Checklist
- [ ] Mon code suit les standards du projet
- [ ] J'ai ajouté des tests
- [ ] Tous les tests passent
- [ ] J'ai mis à jour la documentation
- [ ] Pas de warnings de linting

## Issues liées
Fixes #123
Related to #456
```

## Reporting de bugs

### Avant de créer un bug report

- Vérifiez que le bug n'a pas déjà été reporté
- Essayez de reproduire avec la dernière version
- Collectez les informations nécessaires

### Template de bug report

```markdown
## Description
[Description claire et concise du bug]

## Reproduction
Étapes pour reproduire :
1. 
2. 
3. 

## Comportement attendu
[Ce qui devrait se passer]

## Comportement actuel
[Ce qui se passe réellement]

## Screenshots
[Si applicable]

## Environnement
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- Lotusette version: [e.g., 0.1.0]

## Logs
```
[Coller les logs pertinents]
```

## Informations additionnelles
[Tout autre contexte utile]
```

## Propositions de fonctionnalités

### Template de feature request

```markdown
## Problème résolu
[Quel problème cette fonctionnalité résout-elle ?]

## Solution proposée
[Décrivez votre solution]

## Alternatives considérées
[Quelles alternatives avez-vous envisagées ?]

## Informations additionnelles
[Mockups, exemples, références]
```

## Organisation du développement

### Branches

- `main` : Production stable
- `develop` : Développement actif
- `feature/*` : Nouvelles fonctionnalités
- `fix/*` : Corrections de bugs
- `docs/*` : Documentation
- `refactor/*` : Refactoring

### Workflow Git

```bash
# 1. Synchroniser avec upstream
git fetch upstream
git checkout develop
git merge upstream/develop

# 2. Créer une branche
git checkout -b feature/ma-fonctionnalite

# 3. Développer et commiter
git add .
git commit -m "feat: add amazing feature"

# 4. Pousser et créer PR
git push origin feature/ma-fonctionnalite
```

### Milestones et Labels

Les issues sont organisées par :
- **Milestones** : Phases de la roadmap
- **Labels** :
  - `bug` : Quelque chose ne fonctionne pas
  - `enhancement` : Nouvelle fonctionnalité
  - `documentation` : Documentation
  - `good first issue` : Bon pour débuter
  - `help wanted` : Aide externe souhaitée
  - `priority: high/medium/low`

## Questions ?

- 💬 **Discord** : [Lien à venir]
- 📧 **Email** : [À définir]
- 💡 **Discussions** : Utilisez les GitHub Discussions

## Remerciements

Merci de contribuer à Lotusette ! Chaque contribution, aussi petite soit-elle, est précieuse. 🙏

---

*Ce guide de contribution évoluera avec le projet. N'hésitez pas à suggérer des améliorations !*
