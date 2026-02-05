import csv

from scrapers.brands.minimalist import scrape_minimalist
from scrapers.brands.plum import scrape_plum
from scrapers.brands.dotandkey import scrape_dot_and_key
from scrapers.brands.foxtale import scrape_foxtale
from scrapers.brands.drsheths import scrape_drsheths
from scrapers.brands.dermaco import scrape_dermaco


OUTPUT_FILE = "skincare_products.csv"


def export_all_to_csv():
    all_products = []

    all_products.extend(scrape_minimalist())
    all_products.extend(scrape_plum())
    all_products.extend(scrape_dot_and_key())
    all_products.extend(scrape_foxtale())
    all_products.extend(scrape_drsheths())
    all_products.extend(scrape_dermaco())

    if not all_products:
        return

    fieldnames = [
        "product_href",
        "product_name",
        "product_type",
        "brand",
        "notable_effects",
        "skin_type",
        "price",
        "description",
        "picture_src",
        "source_site",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for product in all_products:
            writer.writerow(product)


if __name__ == "__main__":
    export_all_to_csv()
