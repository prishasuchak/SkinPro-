PRODUCT_TYPE_MAP = {
    # cleanser
    "cleanser": "cleanser",
    "face wash": "cleanser",
    "facewash": "cleanser",
    "facial wash": "cleanser",
    "cleansing oil": "cleanser",
    "cleansing balm": "cleanser",
    "rosewater": "cleanser",

    # moisturizer
    "moisturizer": "moisturizer",
    "moisturiser": "moisturizer",
    "cream": "moisturizer",
    "gel": "moisturizer",
    "lotion": "moisturizer",

    # serum
    "serum": "serum",
    "essence": "serum",

    # sunscreen
    "sunscreen": "sunscreen",
    "sun": "sunscreen",
    "spf": "sunscreen",

    # toner
    "toner": "toner",
    "mist": "toner",

    # mask / pack
    "mask": "mask",
    "sheet mask": "mask",
    "pack": "pack",
    "face pack": "pack",

    # exfoliant
    "exfoliant": "exfoliant",
    "peel": "exfoliant",
    "aha": "exfoliant",
    "bha": "exfoliant",

    # eye care
    "eye": "eye care",
}


BUNDLE_KEYWORDS = [
    "kit",
    "combo",
    "duo",
    "trio",
    "pack",
    "bundle",
    "set",
    "free",
]

def is_bundle(product):
    title = (product.get("title") or "").lower()
    handle = (product.get("handle") or "").lower()

    text = f"{title} {handle}"
    return any(k in text for k in BUNDLE_KEYWORDS)



def normalize_product_type(product):
    """
    Normalize product type into a controlled skincare category.

    Args:
        product (dict): Raw Shopify product JSON

    Returns:
        str: Normalized product type
    """
    raw_type = (product.get("product_type") or "").lower()
    title = (product.get("title") or "").lower()

    text = f"{raw_type} {title}"

    for key, value in PRODUCT_TYPE_MAP.items():
        if key in text:
            return value

    return "other"
