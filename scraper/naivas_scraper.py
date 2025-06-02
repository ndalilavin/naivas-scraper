from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_naivas(search_term):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")  # Uncomment this line if you want to run without opening a browser window

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("✅ Opening website...")
        driver.get("https://naivas.online/")
        wait = WebDriverWait(driver, 40)

        # Give page enough time to load
        time.sleep(10)

        # Handle cookie banner
        print("⏳ Waiting for cookie banner...")
        cookie_labels = ["OK!", "No, thanks", "I want to choose"]
        cookie_button = None

        for label in cookie_labels:
            try:
                cookie_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{label}')]"))
                )
                if cookie_button:
                    cookie_button.click()
                    print(f"✅ Cookie banner dismissed with: {label}")
                    break
            except:
                continue

        if not cookie_button:
            print("⚠️ Cookie banner not found or already dismissed.")

        # Wait for the search input
        try:
            search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
            search_input.clear()
            search_input.send_keys(search_term)
            search_input.send_keys(Keys.RETURN)
            print(f"✅ Search submitted: {search_term}")
        except Exception as e:
            print("❌ Search input not found:", e)
            return

        # Wait for products to load
        time.sleep(10)

        products = driver.find_elements(By.CSS_SELECTOR, ".product-item")

        if not products:
            print("❌ No products found. The page may use JavaScript or changed layout.")
            return

        print(f"✅ Found {len(products)} products:\n")
        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, ".product-title").text
            except:
                title = "N/A"
            try:
                price = product.find_element(By.CSS_SELECTOR, ".product-price").text
            except:
                price = "N/A"
            try:
                img = product.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                img = "N/A"

            print("🔸", title)
            print("   Price:", price)
            print("   Image:", img)
            print("—" * 30)

    except Exception as e:
        print("🚨 ERROR:", e)

    finally:
        driver.quit()
