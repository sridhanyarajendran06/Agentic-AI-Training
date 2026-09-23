"""ReAct agent for the Student Study Planner assessment."""

import json

from config import client, MODEL, banner
from tools import get_subject_hours, calculator


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_subject_hours",
            "description": "Get the number of study-material hours available for a subject.",
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
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a simple arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def execute_tool(name, arguments):
    """Execute the requested tool and return its observation."""

    if name == "get_subject_hours":
        return get_subject_hours(arguments["subject"])

    if name == "calculator":
        return calculator(arguments["expression"])

    return f"Unknown tool: {name}"


def agent(question, max_steps=8):
    """Run a simple ReAct-style tool-calling loop."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a study-planning ReAct agent. "
                "Use tools whenever you need information or calculations. "
                "Do not invent missing study data. "
                "After obtaining the required information, provide a concise final answer."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        # If the model wants to use a tool
        if message.tool_calls:

            messages.append(message)

            for tool_call in message.tool_calls:

                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"step {step}: ACTION -> {name}({arguments})")

                result = execute_tool(name, arguments)

                print(f"step {step}: OBSERVATION -> {result}\n")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    }
                )

            continue

        # No more tools required: final answer
        final_answer = message.content.strip()

        print("FINAL ANSWER:", final_answer)

        return final_answer

    return "The agent reached the maximum number of steps."


if __name__ == "__main__":
    banner("REACT AGENT — STUDENT STUDY PLANNER")

    question = (
        "How many hours of Python study material are available? "
        "If I study 3 hours per day for 5 days, how many hours "
        "of the available Python material can I cover, and what "
        "percentage of the material is that?"
    )

    print("QUESTION:", question, "\n")

    agent(question)