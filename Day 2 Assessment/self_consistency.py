"""Self-consistency experiment for the Day 2 assessment."""

from collections import Counter

from config import client, MODEL, banner


QUESTION = (
    "A student has 20 hours of Python study material. "
    "She studies for 3 hours per day for 5 days. "
    "What percentage of the Python material can she complete?"
)


PROMPT = (
    "Solve the following problem step by step. "
    "Show the calculations clearly and finish with "
    "Final Answer: <answer>.\n\n"
    + QUESTION
)


def extract_answer(text):
    """Extract the final answer from the model response."""

    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()

    return text.splitlines()[-1].strip()


def run_experiment(runs=5, temperature=0.8):
    """Run the same reasoning prompt several times."""

    answers = []

    for run in range(1, runs + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful mathematical reasoning assistant. "
                        "Solve the problem step by step."
                    )
                },
                {
                    "role": "user",
                    "content": PROMPT
                }
            ],
            temperature=temperature
        )

        text = response.choices[0].message.content.strip()
        answer = extract_answer(text)

        print(f"Run {run}: {answer}")

        answers.append(answer)

    return answers


if __name__ == "__main__":

    banner("SELF-CONSISTENCY EXPERIMENT")

    print("QUESTION:")
    print(QUESTION)

    print("\nTemperature = 0.8")
    print("Runs = 5\n")

    answers = run_experiment(runs=5, temperature=0.8)

    counts = Counter(answers)

    print("\n--- OBSERVATION ---")

    for answer, count in counts.items():
        print(f"{count} occurrence(s): {answer}")

    majority_answer, majority_count = counts.most_common(1)[0]

    print(
        f"\nMajority answer: {majority_answer} "
        f"({majority_count} of {len(answers)} runs)"
    )

    print("\nExpected correct answer: 75%")