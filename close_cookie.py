from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def close_cookie_window():
    # Pfad zum heruntergeladenen Chrome Webdriver (oder passen Sie den Pfad entsprechend an)
    driver_path = 'C:/Users/fabif/OneDrive/Desktop/Projects/webscrapping/chromedriver-win32/chromedriver.exe'

    # Erstellen Sie eine Instanz des Chrome-Browsers
    driver = webdriver.Chrome(executable_path=driver_path)

    # Öffnen Sie die svlfg.de-Website
    driver.get("https://www.svlfg.de/")

    try:
        # Warten, bis das Cookie-Fenster angezeigt wird
        cookie_window = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cookieAccept"))
        )

        # Klicken Sie auf das "X" (Schließen-Schaltfläche) oben rechts im Cookie-Fenster
        close_button = cookie_window.find_element_by_xpath("//button[@aria-label='Schließen']")
        close_button.click()

    except Exception as e:
        print("Fehler beim Schließen des Cookie-Fensters:", str(e))

    # Schließen Sie den Browser
    driver.quit()


if __name__ == "__main__":
    close_cookie_window()
