"""Compare unconstrained, JSON mode and schema mode outputs."""

import json

from config import client, MODEL


QUESTION = """
Extract the movie information from this sentence:

"Interstellar has an IMDb rating of 8.7."

Return the movie title, rating platform and rating.
"""


SCHEMA = {
    "type": "object",
    "properties": {
        "movie": {
            "type": "string",
            "description": "Movie title.",
        },
        "platform": {
            "type": "string",
            "enum": ["IMDb", "Rotten Tomatoes"],
            "description": "Rating platform.",
        },
        "rating": {
            "type": "number",
            "description": "Movie rating.",
        },
    },
    "required": ["movie", "platform", "rating"],
    "additionalProperties": False,
}


def print_result(title, response):
    """Print the raw response and parsed result."""

    content = response.choices[0].message.content

    print(f"\n{'=' * 70}")
    print(title)
    print(f"{'=' * 70}")

    print("\nRAW REPLY:")
    print(content)

    print("\nPARSED RESULT:")

    try:
        parsed = json.loads(content)
        print(parsed)
    except (json.JSONDecodeError, TypeError) as error:
        print(f"Could not parse JSON: {error}")


def run_unconstrained():
    """Ask the model without an output constraint."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": QUESTION,
            }
        ],
        max_tokens=200,
    )

    print_result("1. NO CONSTRAINT", response)


def run_json_mode():
    """Ask the model to return valid JSON."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Return the answer as a JSON object.",
                },
                {
                    "role": "user",
                    "content": QUESTION,
                },
            ],
            response_format={"type": "json_object"},
            max_tokens=200,
        )

        print_result("2. JSON MODE", response)

    except Exception as error:
        print("\nJSON MODE ERROR:")
        print(error)


def run_schema_mode():
    """Ask the model to follow a strict JSON schema."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": QUESTION,
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "movie_extraction",
                    "strict": True,
                    "schema": SCHEMA,
                },
            },
            max_tokens=200,
        )

        print_result("3. SCHEMA MODE", response)

    except Exception as error:
        print("\nSCHEMA MODE ERROR:")
        print(error)


if __name__ == "__main__":

    print(
        f"\n=== STRUCTURED OUTPUTS | "
        f"provider: groq | model: {MODEL} ==="
    )

    run_unconstrained()
    run_json_mode()
    run_schema_mode()