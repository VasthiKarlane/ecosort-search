def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

def nettoyer_texte(texte):
    if texte:
        return texte.strip()
    return ""