import requests
from bs4 import BeautifulSoup
from scraper.utils import get_headers, nettoyer_texte

def search_products(keyword):
    url = f"https://www.jumia.ci/catalog/?q={keyword}"
    
    response = requests.get(url, headers=get_headers(), timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    produits = []
    articles = soup.find_all("article", class_="prd")
    
    for article in articles[:5]:
        nom = article.find("h3", class_="name")
        prix = article.find("div", class_="prc")
        lien = article.find("a", class_="core")
        image = article.find("img")
        
        if nom and prix and lien:
            produits.append({
                "nom": nettoyer_texte(nom.text),
                "prix": nettoyer_texte(prix.text),
                "lien": "https://www.jumia.ci" + lien["href"],
                "image": image["data-src"] if image and image.get("data-src") else ""
            })
    
    return produits