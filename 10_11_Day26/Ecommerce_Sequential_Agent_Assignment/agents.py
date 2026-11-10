from tools import search_products
from tools import calculate_order_total
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

def inventory_agent(category):
    print("\n========== INVENTORY AGENT ==========")

    result = search_products(category)

    print(result)

    return result


def pricing_agent(products, quantity, budget):

    print("\n========== PRICING AGENT ==========")

    affordable = []

    for product in products:

        result = calculate_order_total(
            product["id"],
            quantity
        )

        if "error" not in result:

            if result["total_cost"] <= budget:
                affordable.append(result)

    print(affordable)

    return affordable


def recommendation_agent(affordable_products):

    print("\n========== RECOMMENDATION AGENT ==========")

    if len(affordable_products) == 0:

        return "No products satisfy the budget."

    affordable_products.sort(
        key=lambda x:
        (-x["rating"], x["total_cost"])
    )

    best = affordable_products[0]

    recommendation = f"""
Recommended Product : {best['product_name']}
Product ID          : {best['product_id']}
Quantity            : {best['quantity']}
Price               : ₹{best['total_cost']}
Rating              : {best['rating']}

Reason:
Highest rated product available
within the specified budget.
"""

    print(recommendation)

    return recommendation