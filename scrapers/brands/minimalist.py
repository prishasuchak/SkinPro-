from scrapers.brands.shopify import scrape_shopify

def scrape_minimalist(limit=None):
    return scrape_shopify(
        base_url="https://beminimalist.co",
        brand="Minimalist",
        source_site="minimalist",
        limit=limit
    )


if __name__ == "__main__":
    data = scrape_minimalist()

    print("\n--- MINIMALIST PRODUCTS ---")
    print("Total:", len(data))
