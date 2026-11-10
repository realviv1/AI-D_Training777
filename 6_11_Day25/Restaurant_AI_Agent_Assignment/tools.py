import json

from langchain.tools import tool


DATA_FILE = "restaurants.json"


def load_restaurants():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@tool
def search_restaurants(query: str) -> str:
    """
    Search restaurants by cuisine, city, id or restaurant name.
    """

    restaurants = load_restaurants()

    query = query.lower()

    matches = []

    for r in restaurants:

        if (
            query in r["name"].lower()
            or query in r["cuisine"].lower()
            or query in r["location"].lower()
            or query in r["id"].lower()
        ):
            matches.append(
                f"""
Restaurant ID: {r['id']}
Name: {r['name']}
Cuisine: {r['cuisine']}
Location: {r['location']}
Price Per Person: ₹{r['price_per_person']}
Available Seats: {r['available_seats']}
"""
            )

    if not matches:
        return "No matching restaurants found."

    return "\n".join(matches[:20])


@tool
def calculate_dining_cost(
    restaurant_id: str,
    guests: int
) -> str:
    """
    Calculate dining cost using restaurant id and guest count.
    """

    if guests < 1 or guests > 20:
        return "Guest count must be between 1 and 20."

    restaurants = load_restaurants()

    for r in restaurants:

        if r["id"].lower() == restaurant_id.lower():

            total = r["price_per_person"] * guests

            return (
                f"Restaurant: {r['name']}\n"
                f"Guests: {guests}\n"
                f"Price Per Person: ₹{r['price_per_person']}\n"
                f"Estimated Total Cost: ₹{total}"
            )

    return "Restaurant not found."