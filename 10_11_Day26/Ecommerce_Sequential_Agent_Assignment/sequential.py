import asyncio
import re

from agents import inventory_agent
from agents import pricing_agent
from agents import recommendation_agent


def extract_info(user_request):

    category = None
    quantity = 1
    budget = 999999999

    categories = [
        "laptop",
        "smartphone",
        "tablet",
        "monitor",
        "headphone",
        "printer",
        "accessory"
    ]

    text = user_request.lower()

    for item in categories:
        if item in text:
            category = item
            break

    qty_match = re.search(r"(\d+)", text)

    if qty_match:
        quantity = int(qty_match.group(1))

    budget_match = re.search(
        r"(\d[\d,]*)",
        user_request
    )

    if budget_match:
        budget = int(
            budget_match.group(1).replace(",", "")
        )

    return category, quantity, budget


async def workflow(user_request):

    category, quantity, budget = extract_info(
        user_request
    )

    inventory_result = inventory_agent(
        category
    )

    if isinstance(inventory_result, dict):
        print(inventory_result["message"])
        return

    pricing_result = pricing_agent(
        inventory_result,
        quantity,
        budget
    )

    recommendation = recommendation_agent(
        pricing_result
    )

    print("\n========== FINAL RESULT ==========")

    print(recommendation)


async def main():

    request = input(
        "\nEnter Customer Request:\n"
    )

    await workflow(request)


if __name__ == "__main__":
    asyncio.run(main())