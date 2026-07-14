from scraper.jumia_scraper import search_products

def test_search_products():
    resultats = search_products("bouteille")
    
    # Vérifier qu'on a des résultats
    assert len(resultats) > 0, "Aucun produit trouvé"
    
    # Vérifier que chaque produit a les 4 champs
    for produit in resultats:
        assert "nom" in produit, "Champ nom manquant"
        assert "prix" in produit, "Champ prix manquant"
        assert "lien" in produit, "Champ lien manquant"
        assert "image" in produit, "Champ image manquant"
        
        # Vérifier que les champs ne sont pas vides
        assert produit["nom"] != "", "Nom vide"
        assert produit["prix"] != "", "Prix vide"
        assert produit["lien"].startswith("https://"), "Lien invalide"
    
    print("✅ Tous les tests sont passés !")

test_search_products()