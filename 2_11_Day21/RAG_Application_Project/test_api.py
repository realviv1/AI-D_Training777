from ai_answer import get_answer

context = """
Full-time employees receive 16 days of paid annual leave each calendar year.
Employees are required to work from the office on Tuesdays and Thursdays.
"""

question = "How many annual leave days do employees receive?"

answer = get_answer(question, context)

print("Final Answer:")
print(answer)