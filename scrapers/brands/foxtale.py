from scrapers.brands.shopify import scrape_shopify


def scrape_foxtale(limit=None):
    return scrape_shopify(
        base_url="https://foxtale.in",
        brand="Foxtale",
        source_site="foxtale",
        limit=limit
    )


if __name__ == "__main__":
    data = scrape_foxtale()

    print("\n--- FOXTALE PRODUCTS ---")
    print("Total:", len(data))
