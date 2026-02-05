from scrapers.brands.shopify import scrape_shopify


def scrape_dermaco(limit=None):
    return scrape_shopify(
        base_url="https://thedermaco.com",
        brand="The Derma Co",
        source_site="dermaco",
        limit=limit
    )


if __name__ == "__main__":
    data = scrape_dermaco()
    print("Total:", len(data))
