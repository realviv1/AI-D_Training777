import json
from dotenv import load_dotenv
import os
from openai import OpenAI

from tools import search_books, reserve_book

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Search books in library",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": "Reserve a book",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer"
                    },
                    "customer_name": {
                        "type": "string"
                    }
                },
                "required": [
                    "book_id",
                    "customer_name"
                ]
            }
        }
    }
]

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        tools=tools
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        print("\nSelected Tool:", tool_name)

        args = json.loads(
            tool_call.function.arguments
        )

        if tool_name == "search_books":

            result = search_books(
                args["keyword"]
            )

        elif tool_name == "reserve_book":

            result = reserve_book(
                args["book_id"],
                args["customer_name"]
            )

        second_response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                },
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            ]
        )

        print(
            "\nAssistant:",
            second_response.choices[0].message.content
        )

    else:
        print(
            "\nAssistant:",
            message.content
        )