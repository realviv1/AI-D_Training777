from dotenv import load_dotenv


from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import InMemorySaver

from langgraph.prebuilt import create_react_agent

from tools import (
    search_restaurants,
    calculate_dining_cost
)

from guardrails import (
    validate_user_input,
    detect_pii,
    redact_pii
)



memory = InMemorySaver()

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)
SYSTEM_PROMPT = """
You are a Restaurant Reservation Assistant.

Rules:
1. Only answer restaurant related queries.
2. Never invent restaurants.
3. Never invent prices.
4. Never invent availability.
5. Use tool results only.
6. Remember previous restaurant selections.
7. Remember guest counts.
8. Remember previous cost calculations.
"""


agent = create_react_agent(
    model=llm,
    tools=[
        search_restaurants,
        calculate_dining_cost
    ],
    checkpointer=memory,
    prompt=SYSTEM_PROMPT
)


config = {
    "configurable": {
        "thread_id": "restaurant_chat"
    }
}


print("=" * 60)
print("Restaurant AI Agent")
print("Type /new to reset memory")
print("Type quit to exit")
print("=" * 60)


while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        break

    if user_input.lower() == "/new":

        config = {
            "configurable": {
                "thread_id": "new_chat"
            }
        }

        print("Conversation cleared.")
        continue

    valid, message = validate_user_input(
        user_input
    )

    if not valid:
        print(f"Agent: {message}")
        continue

    emails, phones = detect_pii(user_input)

    if emails or phones:
        print(
            "Agent: PII detected "
            "(email or phone number)."
        )

    response = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    user_input
                )
            ]
        },
        config=config
    )

    final_answer = response["messages"][-1].content

    final_answer = redact_pii(
        final_answer
    )

    print("\nAgent:")
    print(final_answer)

    print("\n" + "=" * 60)