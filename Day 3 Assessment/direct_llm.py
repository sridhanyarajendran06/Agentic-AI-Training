from config import client, MODEL

questions = [
    "How many hours of Python study material are available in my study database?",
    "If I study 3 hours per day for 5 days, how many hours will I study in total?",
    "What is the capital of France?"
]

for question in questions:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only your own knowledge. "
                    "You do not have access to any external tools or databases."
                )
            },
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    print("\nQ:", question)
    print("A:", response.choices[0].message.content)