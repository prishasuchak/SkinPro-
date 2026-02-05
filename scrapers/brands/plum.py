from scrapers.brands.shopify import scrape_shopify

def scrape_plum(limit=None):
    return scrape_shopify(
        base_url="https://plumgoodness.com",
        brand="Plum",
        source_site="plum",
        limit=limit
    )


if __name__ == "__main__":
    data = scrape_plum()

    print("\n--- PLUM PRODUCTS ---")
    print("Total:", len(data))
