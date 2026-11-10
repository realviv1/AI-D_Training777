import json


def load_products():
    with open("products.json", "r", encoding="utf-8") as file:
        return json.load(file)


def search_products(query):
    products = load_products()

    query = query.lower()

    matches = []

    for product in products:
        if (
            query in product["name"].lower()
            or query in product["category"].lower()
        ):
            matches.append(
                {
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "stock": product["stock"],
                    "rating": product["rating"]
                }
            )

    if not matches:
        return {
            "message": f"No products found for '{query}'."
        }

    return matches


def calculate_order_total(product_id, quantity):
    products = load_products()

    if quantity <= 0:
        return {
            "error": "Quantity must be greater than zero."
        }

    for product in products:

        if product["id"] == product_id:

            if quantity > product["stock"]:
                return {
                    "error":
                    f"Insufficient stock. Available: {product['stock']}"
                }

            total = product["price"] * quantity

            return {
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": quantity,
                "unit_price": product["price"],
                "total_cost": total,
                "rating": product["rating"]
            }

    return {
        "error": f"Product {product_id} not found."
    }