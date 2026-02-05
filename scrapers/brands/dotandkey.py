from scrapers.brands.shopify import scrape_shopify


def scrape_dot_and_key(limit=None):
    return scrape_shopify(
        base_url="https://dotandkey.com",
        brand="Dot & Key",
        source_site="dotandkey",
        limit=limit
    )


if __name__ == "__main__":
    data = scrape_dot_and_key()

    print("\n--- DOT & KEY PRODUCTS ---")
    print("Total:", len(data))
