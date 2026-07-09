import requests
from bs4 import BeautifulSoup

def search_products(keyword):
    url = f"https://www.jumia.ci/catalog/?q={keyword}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    produits = []
    articles = soup.find_all("article", class_="prd")
    
    for article in articles[:5]:
        nom = article.find("h3", class_="name")
        prix = article.find("div", class_="prc")
        lien = article.find("a", class_="core")
        
        if nom and prix and lien:
            produits.append({
                "nom": nom.text.strip(),
                "prix": prix.text.strip(),
                "lien": "https://www.jumia.ci" + lien["href"]
            })
    
    return produits