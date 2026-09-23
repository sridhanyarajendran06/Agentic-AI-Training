import json

from config import client, MODEL
from tools import get_subject_hours


TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_subject_hours",
            "description": (
                "Look up the number of study-material hours available "
                "for a subject in the private study database."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The subject name, such as Python, DBMS, or Mathematics."
                    }
                },
                "required": ["subject"]
            }
        }
    }
]


questions = [
    "How many hours of Python study material are available in my study database?",
    "If I study 3 hours per day for 5 days, how many hours will I study in total?",
    "What is the capital of France?"
]


for question in questions:
    print("\nQ:", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question. You have access to one tool "
                    "that can look up private study-database information."
                )
            },
            {"role": "user", "content": question}
        ],
        tools=TOOL_SCHEMA,
        temperature=0
    )

    message = response.choices[0].message

    if message.tool_calls:
        for call in message.tool_calls:
            print(
                "TOOL CALL:",
                call.function.name,
                call.function.arguments
            )

            arguments = json.loads(call.function.arguments)

            if call.function.name == "get_subject_hours":
                result = get_subject_hours(**arguments)

                print("TOOL RESULT:", result)

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Answer the user's question using the tool result. "
                            "Do not invent private database information."
                        )
                    },
                    {"role": "user", "content": question},
                    {
                        "role": "assistant",
                        "content": message.content or "",
                        "tool_calls": [
                            {
                                "id": call.id,
                                "type": "function",
                                "function": {
                                    "name": call.function.name,
                                    "arguments": call.function.arguments
                                }
                            }
                        ]
                    },
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result)
                    }
                ]

                final_response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0
                )

                print(
                    "FINAL ANSWER:",
                    final_response.choices[0].message.content
                )
    else:
        print("TOOL CALL: None")
        print("FINAL ANSWER:", message.content)