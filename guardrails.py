SHOPPING_KEYWORDS = {
    "buy",
    "purchase",
    "order",
    "shop",
    "product",
    "products",
    "price",
    "cost",
    "rating",
    "review",
    "organic",
    "honey",
    "oil",
    "almond",
    "coffee",
    "tea",
    "snack",
    "milk",
    "rice",
    "oats",
    "similar",
    "recommend",
    "recommendation",
    "store",
    "item",
    "items",
}


def is_shopping_related(message):
    text = message.lower()

    return any(keyword in text for keyword in SHOPPING_KEYWORDS)


def guardrail(message):
    if is_shopping_related(message):
        return True, ""

    return False, (
        "I'm your shopping assistant, so I can help you find products, "
        "compare prices, check ratings, remember your preferences, "
        "and place orders. What would you like to shop for?"
    )