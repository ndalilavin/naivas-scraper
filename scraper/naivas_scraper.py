from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_naivas(query="blue band"):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")  # Uncomment for headless mode

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("✅ Opening website...")
        driver.get("https://naivas.online/")

        # Wait for and enter the search query
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query)
        search_box.submit()
        print(f"🔍 Searched for '{query}'...")

        # Wait for results
        time.sleep(5)

        # Try scraping product titles
        products = driver.find_elements(By.CSS_SELECTOR, ".product-box")

        if not products:
            print("❌ No products found. The page may use JavaScript or has changed structure.")
            return

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, ".product-title").text
            except:
                title = "N/A"
            try:
                price = product.find_element(By.CSS_SELECTOR, ".price").text
            except:
                price = "N/A"

            print("------")
            print("Name:", title)
            print("Price:", price)

    except Exception as e:
        print("🚨 ERROR:", e)

    finally:
        driver.quit()
        print("✅ Done.")

if __name__ == "__main__":
    scrape_naivas()
