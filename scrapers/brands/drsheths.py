from scrapers.brands.shopify import scrape_shopify


def scrape_drsheths(limit=None):
    return scrape_shopify(
        base_url="https://drsheths.com",
        brand="Dr Sheth’s",
        source_site="drsheths",
        limit=limit
    )


if __name__ == "__main__":
    data = scrape_drsheths()
    print("Total:", len(data))
