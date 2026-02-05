import requests
import time

from utils.skin_logic import infer_skin_type, infer_concerns
from utils.product_type import normalize_product_type, is_bundle


def scrape_shopify(
    base_url: str,
    brand: str,
    source_site: str,
    limit: int | None = None,
    sleep_time: float = 0.7,
    max_pages: int = 15,
):
    """
    Generic Shopify scraper using products.json with cursor-based pagination.

    Behavior:
    - Skips pages on HTTP 429
    - Removes kits / combos / duos / trios / freebies
    - Deduplicates by handle
    """

    since_id = 0
    page_count = 0
    all_results = []
    seen_handles = set()

    print(f"\nStarting Shopify scrape for: {brand}")

    while page_count < max_pages:
        url = f"{base_url}/products.json?since_id={since_id}"
        print(f"\nRequesting URL: {url}")

        response = requests.get(url, timeout=20)

        if response.status_code == 429:
            print("HTTP 429 received. Skipping this page.")
            break

        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
            break

        data = response.json()
        products = data.get("products", [])

        if not products:
            print("No more products returned. Ending pagination.")
            break

        page_count += 1
        print(f"Page {page_count}: received {len(products)} products")

        last_id = products[-1].get("id")

        page_added = 0
        page_skipped_bundle = 0
        page_skipped_duplicate = 0

        for p in products:
            handle = p.get("handle")
            if not handle:
                continue

            if handle in seen_handles:
                page_skipped_duplicate += 1
                continue

            if is_bundle(p):
                page_skipped_bundle += 1
                continue

            seen_handles.add(handle)

            body_html = p.get("body_html") or ""

            price = None
            if p.get("variants"):
                price = p["variants"][0].get("price")

            image = None
            if p.get("images"):
                image = p["images"][0].get("src")

            all_results.append({
                "product_href": f"{base_url}/products/{handle}",
                "product_name": p.get("title"),
                "product_type": normalize_product_type(p),
    
                "notable_effects": ", ".join(infer_concerns(body_html)),
                "skin_type": ", ".join(infer_skin_type(body_html)),
                "price": price,
                "picture_src": image,
               
            })

            page_added += 1

            if limit and len(all_results) >= limit:
                print(f"Product limit reached: {limit}")
                return all_results

        since_id = last_id

        print(
            f"Page {page_count} summary → "
            f"added: {page_added}, "
            f"bundles skipped: {page_skipped_bundle}, "
            f"duplicates skipped: {page_skipped_duplicate}"
        )

        print(f"Updated since_id to: {since_id}")

        time.sleep(sleep_time)

    print(
        f"\nFinished scraping {brand}. "
        f"Total valid products collected: {len(all_results)}"
    )

    return all_results




