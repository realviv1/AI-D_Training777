from openai import OpenAI

# Paste your OpenRouter API Key here
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)


def get_answer(question, context):
    try:
        prompt = f"""
You are a helpful assistant.

Answer ONLY from the provided context.

Context:
{context}

Question:
{question}

Rules:
1. Use only the information present in the context.
2. Do not make assumptions.
3. If the answer is not present, reply:
'I cannot find the answer in the provided documents.'
"""

        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=300
        )

        answer = response.choices[0].message.content

        print("\n====================")
        print("AI ANSWER:")
        print(answer)
        print("====================\n")

        return answer

    except Exception as e:
        print("\n====================")
        print("ERROR:")
        print(str(e))
        print("====================\n")

        return f"Error: {str(e)}"