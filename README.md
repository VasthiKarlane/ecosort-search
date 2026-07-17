# ♻️ EcoSort-Search

Application web qui aide les utilisateurs à trier leurs déchets : l'utilisateur saisit le nom d'un produit, l'application le recherche sur **Jumia**, puis un modèle de **Deep Learning** identifie la matière de son emballage et affiche la consigne de tri officielle correspondante.

Projet de fin de module ISE2 - ML2.

---

## 🎯 Fonctionnement

1. L'utilisateur saisit le nom d'un produit (ex : *"bouteille"*).
2. L'application scrape Jumia et propose 3 à 5 résultats correspondants.
3. L'utilisateur sélectionne un produit.
4. Le modèle de classification analyse le produit (image + nom) et détermine sa catégorie de tri.
5. L'interface affiche le résultat avec la couleur de la poubelle correspondante.

## 🗂️ Catégories de tri

| Catégorie | Couleur | Exemples | Matières (dataset) |
| :--- | :--- | :--- | :--- |
| Poubelle jaune | 🟡 | Bouteilles plastique, canettes, boîtes de conserve, cartons | `plastic`, `metal`, `cardboard` |
| Poubelle verte | 🟢 | Bouteilles/pots en verre | `glass` |
| Poubelle bleue | 🔵 | Papiers, journaux, magazines | `paper` |
| Bac électronique (D3E) | ⚫ | Smartphones, chargeurs, écouteurs, petit électroménager | Détection par mots-clés sur le nom du produit |
| Poubelle marron/noire | 🟤 | Déchets résiduels non recyclables | `trash` |

## 📁 Structure du projet

```
ecosort-search/
├── app/                # Application web Flask
│   ├── main.py          # Routes : recherche, sélection, classification
│   ├── static/style.css
│   └── templates/       # index.html, results.html, result.html
├── data/
│   ├── raw/            # Dataset Kaggle "Garbage Classification" (non versionné)
│   └── processed/
├── model/
│   ├── config.py        # Hyperparamètres, chemins, mapping des catégories
│   ├── preprocessing.py  # Génération des datasets d'entraînement/validation
│   ├── train.py          # Entraînement (Transfer Learning MobileNetV2)
│   ├── evaluate.py        # Évaluation : rapport + matrice de confusion
│   ├── classify.py         # Classification finale (modèle IA + détection D3E)
│   └── saved_model/         # Modèle entraîné (non versionné)
├── scraper/
│   ├── jumia_scraper.py  # Recherche de produits sur Jumia
│   └── utils.py           # Fonctions utilitaires (headers, nettoyage de texte)
├── notebooks/
│   └── exploration.ipynb # Exploration du dataset
├── tests/
│   └── test_scraper.py   # Tests du scraper
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Installation

```bash
git clone https://github.com/VasthiKarlane/ecosort-search.git
cd ecosort-search
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Le dataset [Garbage Classification](https://www.kaggle.com/code/muhammedabdulazeem/garbage-classification) doit être téléchargé manuellement et placé dans `data/raw/` (un sous-dossier par classe : `plastic`, `glass`, `metal`, `paper`, `cardboard`, `trash`).

## 🧠 Entraîner et évaluer le modèle

```bash
cd model
python train.py       # entraîne le modèle et le sauvegarde dans saved_model/
python evaluate.py    # génère le rapport de classification et la matrice de confusion
python classify.py    # test rapide de classification sur une image du dataset
```

Le modèle actuel (Transfer Learning sur `MobileNetV2`) atteint **~75% d'accuracy** en validation.

## 🕸️ Scraper Jumia

```python
from scraper.jumia_scraper import search_products

resultats = search_products("bouteille")
```

Lancer les tests :

```bash
pytest tests/
```

## Lancer l'application en local

```bash
cd app
python main.py
```

L'application est accessible sur [http://localhost:8501](http://localhost:8501). Elle nécessite qu'un modèle entraîné soit présent dans `model/saved_model/modele_eco_sort.h5` (voir section précédente).

## 🐳 Docker

L'application (interface web Flask + modèle + scraper) est packagée dans un `Dockerfile`, exécutable avec :

```bash
docker build -t ecosort .
docker run -p 8501:8501 ecosort
```

ou avec Docker Compose :

```bash
docker-compose up -d --build
```

L'application est alors accessible sur [http://localhost:8501](http://localhost:8501). Le modèle entraîné (`model/saved_model/modele_eco_sort.h5`) est versionné dans le dépôt et inclus directement dans l'image au build.

## 🛠️ État d'avancement

- [x] Jalon 1 — Entraînement de l'IA (prétraitement, modèle, évaluation, mapping des catégories, détection D3E)
- [x] Jalon 2 — Scraping Jumia (recherche de produits + tests)
- [x] Jalon 2 — Interface web (Flask)
- [x] Jalon 2 — Containerisation Docker

## 👥 Équipe

Développement en collaboration via des branches dédiées (`feature/model-training`, `feature/jumia-scraper`, `feature/app-docker`) et des Pull Requests relues avant fusion sur `main`.
