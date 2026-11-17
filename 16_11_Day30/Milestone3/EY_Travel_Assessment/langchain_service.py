import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(

    api_key=os.getenv("OPENROUTER_API_KEY"),

    base_url="https://openrouter.ai/api/v1",

    model="qwen/qwen-2.5-7b-instruct"
)

def generate_advice(

    trip_details,
    weather_details,
    question
):

    prompt = f"""
You are a travel assistant.

Question:
{question}

Trip Details:
{trip_details}

Weather Details:
{weather_details}

Generate:

1. Weather Summary
2. Travel Advice
3. 4 Packing Suggestions

Keep response concise.
"""

    result = llm.invoke(prompt)

    return result.content