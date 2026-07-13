"""
Application web EcoSort-Search (Flask).
Recherche un produit sur Jumia puis affiche sa consigne de tri officielle.
"""
import os
import sys
import tempfile

import requests
from flask import Flask, redirect, render_template, request, url_for

# `scraper` et `model` sont a la racine du depot, hors du package `app`.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "model"))

from scraper.jumia_scraper import search_products  # noqa: E402
import classify  # noqa: E402

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "").strip()
    if not keyword:
        return redirect(url_for("index"))

    produits = search_products(keyword)
    return render_template("results.html", keyword=keyword, produits=produits)


@app.route("/classify", methods=["POST"])
def classify_product():
    nom = request.form.get("nom", "")
    image_url = request.form.get("image", "")
    lien = request.form.get("lien", "")

    try:
        if classify.is_d3e(nom):
            resultat = {
                "category": "D3E",
                "color": classify.config.CATEGORY_COLORS["D3E"],
                "detected_material": None,
                "confidence": None,
            }
        elif not image_url:
            raise ValueError("Aucune image disponible pour ce produit.")
        else:
            image_path = _download_image(image_url)
            try:
                resultat = classify.predict_category(image_path, product_name=nom)
            finally:
                os.remove(image_path)
    except Exception as exc:
        return render_template("result.html", nom=nom, lien=lien, image=image_url, erreur=str(exc))

    return render_template("result.html", nom=nom, lien=lien, image=image_url, resultat=resultat)


def _download_image(image_url):
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()

    suffix = os.path.splitext(image_url)[1].split("?")[0] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(response.content)
        return tmp.name


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)
