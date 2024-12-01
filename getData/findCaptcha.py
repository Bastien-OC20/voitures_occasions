from playwright.sync_api import sync_playwright

def find_captcha(page):
    # Attendre que l'élément captcha soit présent
    try:
        captcha_element = page.wait_for_selector(
            "captcha__puzzle", timeout=60000
        )  # Attendre jusqu'à 10 secondes
        if captcha_element:
            captcha_html = captcha_element.inner_html()
            print("Captcha trouvé :")
            print(captcha_html)
        else:
            print("Élément captcha non trouvé.")
    except Exception as e:
        print(f"Erreur lors de la recherche du captcha : {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Naviguer vers la page cible
    url = "https://www.leboncoin.fr/c/voitures"
    page.goto(url)
    page.wait_for_timeout(6000)  # Attendre que la page se charge

    # Rechercher et récupérer la balise HTML du captcha
    find_captcha(page)

    # Fermer le navigateur
    browser.close()
