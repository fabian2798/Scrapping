import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import close_cookie

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(url):
    # Eine leere Liste zum Speichern der gesammelten Daten
    data = []

    # Funktion zum Abrufen des HTML-Inhalts einer Seite
    def get_page_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            logging.error(f"Error {response.status_code} while retrieving {url}")
            raise Exception(f"Error {response.status_code} while retrieving {url}")

    # Funktion zum Parsen der Seite und Extrahieren relevanter Daten
    def parse_page_content(content):
        soup = BeautifulSoup(content, 'html.parser')
        # Hier können Sie die spezifischen HTML-Elemente und -Klassen identifizieren, die Sie extrahieren möchten.
        # Verwenden Sie BeautifulSoup-Methoden, um die Daten zu finden und in die data-Liste einzufügen.

        # Beispiel: Titel extrahieren
        title_element = soup.find('h1', class_='title')
        title = title_element.text.strip() if title_element else ""
        if title:
            logging.info(f"Extracted title: {title}")
        else:
            logging.warning(f"No title found on the page: {url}")
        # Beispiel: Beschreibung extrahieren
        description_element = soup.find('p', class_='description')
        description = description_element.text.strip() if description_element else ""
        if description:
            logging.info(f"Extracted title: {description}")
        else:
            logging.warning(f"No description found on the page: {url}")
        # Die extrahierten Daten zur data-Liste hinzufügen
        data.append({
            "title": title,
            "description": description
        })

    # Haupt-Scraping-Logik für die gegebene URL und alle Unterseiten
    def scrape_recursive(url):
        logging.info(f"Scrapping page: {url}")
        content = get_page_content(url)
        soup = BeautifulSoup(content, 'html.parser')
        parse_page_content(content)

        # Wenn es Unterseiten gibt, diese ebenfalls durchsuchen
        links = soup.find_all('a', href=True)
        for link in links:
            absolute_url = urljoin(url, link['href'])
            if absolute_url.startswith(url):  # Prüfen, ob der Link zur gleichen Website gehört
                scrape_recursive(absolute_url)

    # Starten Sie das rekursive Scraping
    logging.info("Starting web scrapping- - -")
    scrape_recursive(url)
    logging.info("Webscraping completed.")

    return data

def write_data_to_file(data):
    with open("scraped_data.txt", "w", encoding="utf-8") as file:
        for item in data:
            file.write(f"Title: {item['title']}\n")
            file.write(f"Description: {item['description']}\n")
            file.write("-" * 50 + "\n")


if __name__ == "__main__":
    target_url = "https://www.svlfg.de"  # Ihre Zielwebsite hier eingeben
    close_cookie.close_cookie_window() # Schließen des Cookie-Fensters
    scraped_data = scrape_website(target_url) # Scraping der Daten
    logging.info("Scraping data:")
    logging.info(scraped_data)

    # Daten in Textdatei schreiben
    write_data_to_file(scraped_data)
