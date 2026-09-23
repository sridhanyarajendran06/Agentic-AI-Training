"""Compare Direct Prompting and Chain-of-Thought on the same scenario."""

from config import client, MODEL, banner


QUESTIONS = [
    # Reasoning-only question
    (
        "You have 3 hours available each day for 5 days. "
        "If you spend 2 hours per day studying Python, "
        "how many total hours remain for other subjects?"
    ),

    # Question requiring information from a tool
    (
        "How many hours of Python study material are available "
        "in the study database?"
    ),

    # Multi-step reasoning question
    (
        "A student has 20 hours of Python study material. "
        "If she studies for 3 hours per day for 5 days, "
        "what percentage of the Python material can she complete?"
    ),
]


DIRECT_PROMPT = (
    "You are a helpful study-planning assistant. "
    "Answer the question directly using only the information "
    "provided in the question or your existing knowledge. "
    "You do not have access to external tools. "
    "Give the final answer clearly without showing your reasoning."
)


COT_PROMPT = (
    "You are a helpful study-planning assistant. "
    "Solve the question step by step using only the information "
    "provided in the question or your existing knowledge. "
    "You do not have access to external tools. "
    "Show the calculation in numbered steps. "
    "If required information is missing, clearly state that "
    "you cannot verify it rather than inventing a value. "
    "End with: Final Answer: <answer>"
)


def ask(system_prompt, question):
    """Send one question to the model."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("DIRECT PROMPTING vs CHAIN-OF-THOUGHT")

    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}")
        print(question)

        print("\n--- DIRECT PROMPTING ---")
        print(ask(DIRECT_PROMPT, question))

        print("\n--- CHAIN-OF-THOUGHT ---")
        print(ask(COT_PROMPT, question))

        print()