# Détectez la Nourriture, les Boissons et Plus avec le Deep Learning

Ce projet utilise le Deep Learning pour analyser des images et déterminer si elles contiennent de la nourriture, des boissons ou d'autres éléments. Il peut être particulièrement utile pour surveiller les réseaux sociaux.

## Fonctionnalités

- **Détection de catégorie** : Identifie si l'image soumise est liée à de la nourriture, une boisson ou autre.
- **Prétraitement de l'image** : Applique diverses techniques de nettoyage et de normalisation de l'image pour la préparer à l'analyse.
- **Analyse d'image** : Utilise un modèle de Deep Learning pour prédire la catégorie de l'image (nourriture, boisson, etc.).

## Prérequis

- Python 3.x

## Installation

Clonez le dépôt :

```
git clone git@github.com:maxime9446/Kookeat-ia.git
```

```
git submodule update --init --recursive
```

## Configuration de l'environnement

Créez et activez un environnement virtuel :

```
python -m venv mon_env
source mon_env/bin/activate  # Unix/MacOS
.\venv\Scripts\activate   # Windows
```

Installez les dépendances :

```
pip install -r requirements.txt
```

## Utilisation

Lancez l'application avec FastAPI :

```
uvicorn main:app --reload
```

Visitez http://127.0.0.1:8000 dans votre navigateur.

### Endpoints API

- **POST /predict/** : Soumettez une image pour prédiction. Exemple de corps de requête :

  ```
  {
      "image": "Votre image encodée en base64 ou l'URL de l'image..."
  }
  ```

- **GET /healthcheck** : Vérifiez l'état de fonctionnement de l'API.

## Construction du modèle

Le modèle de Deep Learning est construit à l'aide du notebook Jupyter `generate_model.ipynb`. Les données utilisées pour l'entraînement proviennent d'un ensemble de données d'images classées par catégories (`data`). Le modèle entraîné doit être placé à la racine du projet.