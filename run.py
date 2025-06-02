from scraper.naivas_scraper import scrape_naivas

if __name__ == "__main__":
    print("✅ Starting scraper...")
    try:
        scrape_naivas("Blue Band")
    except Exception as e:
        print("💥 Unexpected error:", e)
    print("✅ Done.")
