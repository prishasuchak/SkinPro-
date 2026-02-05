SKIN_TYPES = {
    "oily": ["oily", "oil control", "acne prone"],
    "dry": ["dry", "very dry", "dehydrated"],
    "combination": ["combination"],
    "sensitive": ["sensitive", "gentle", "fragrance free"],
    "normal": ["normal"]
}

CONCERNS = {
    "acne": [
        "acne", "pimple", "breakout", "blemish"
    ],
    "blackheads": [
        "blackhead", "black head"
    ],
    "whiteheads": [
        "whitehead", "white head"
    ],
    "open_pores": [
        "open pores", "large pores", "enlarged pores", "pores"
    ],
    "pigmentation": [
        "pigmentation", "dark spot", "uneven tone", "hyperpigmentation"
    ],
    "dark_under_eyes": [
        "dark under eye", "dark circles", "under eye darkness"
    ],
    "puffy_eyes": [
        "puffy eyes", "eye puffiness", "under eye bags"
    ],
    "redness": [
        "redness", "irritation", "inflamed", "rosacea"
    ],
    "dullness": [
        "dull", "tired skin", "glow", "tanned"
    ],
    "dryness": [
        "dry", "dehydrated", "flaky", "hydration"
    ],
    "oil_control": [
        "oil control", "sebum", "excess oil"
    ],
    "anti_aging": [
        "anti aging", "wrinkle", "fine line", "aging"
    ],
    "sun_protection": [
        "spf", "sunscreen", "uv", "sun protection"
    ]
}

def infer_skin_type(text):
    if not text:
        return ["unknown"]

    text = text.lower()
    found = []

    for skin, keywords in SKIN_TYPES.items():
        for kw in keywords:
            if kw in text:
                found.append(skin)
                break

    return list(set(found)) if found else ["unknown"]


def infer_concerns(text):
    if not text:
        return ["general"]

    text = text.lower()
    found = []

    for concern, keywords in CONCERNS.items():
        for kw in keywords:
            if kw in text:
                found.append(concern)
                break

    return list(set(found)) if found else ["general"]

