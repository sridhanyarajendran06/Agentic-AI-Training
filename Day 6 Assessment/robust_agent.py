"""Robust tool-calling agent for the Day 6 assessment."""

import json
from collections import defaultdict

from config import client, MODEL
from tools import SCHEMAS, TOOL_FUNCTIONS
from validator import validate_arguments


MAX_STEPS = 6
REPEAT_LIMIT = 3
INITIAL_MAX_TOKENS = 300
RETRY_MAX_TOKENS = 700


SYSTEM_PROMPT = """
You are a reliable movie recommendation assistant.

You can use tools to look up movie ratings and calculate watch scores.

Available movies:
- Interstellar
- Inception
- Dune

Available rating platforms:
- IMDb
- Rotten Tomatoes

Rules:
1. Never invent movie ratings.
2. Use get_movie_rating when a rating is required.
3. Use calculate_watch_score when a calculation is required.
4. You may request multiple independent tool calls in one response.
5. If a tool returns an error, use that message to recover.
6. Give a concise final answer.
"""


def handle_tool_call(tool_call, log=True):
    """Safely parse, validate and execute one model-generated tool call."""

    tool_name = tool_call.function.name
    raw_arguments = tool_call.function.arguments

    # Stage 1: Parse JSON
    try:
        arguments = json.loads(raw_arguments)
    except (json.JSONDecodeError, TypeError) as error:
        return f"Tool argument JSON error: {error}"

    # Stage 2: Look up the tool
    if tool_name not in TOOL_FUNCTIONS:
        return f"Unknown tool: {tool_name}"

    # Stage 3: Validate arguments
    validation_error = validate_arguments(tool_name, arguments)

    if validation_error is not None:
        return f"Validation error: {validation_error}"

    # Stage 4: Execute the tool
    try:
        result = TOOL_FUNCTIONS[tool_name](**arguments)
        return str(result)
    except Exception as error:
        return f"Tool execution error: {error}"


def agent(question, max_steps=MAX_STEPS, verbose=True):
    """Run the complete tool-calling loop."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    tools = list(SCHEMAS.values())

    repeated_calls = defaultdict(int)
    max_tokens = INITIAL_MAX_TOKENS

    for step in range(1, max_steps + 1):

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=max_tokens,
            )
        except Exception as error:
            return f"API error: {error}"

        choice = response.choices[0]
        message = choice.message
        finish_reason = choice.finish_reason

        # Retry truncated responses with a larger token budget.
        if finish_reason == "length":
            if max_tokens < RETRY_MAX_TOKENS:
                max_tokens = RETRY_MAX_TOKENS

                if verbose:
                    print(
                        f"   step {step}: response truncated; "
                        f"retrying with max_tokens={max_tokens}"
                    )

                continue

            return "Stopped: response remained truncated after retry."

        # No tool call means the model has produced its final answer.
        if not message.tool_calls:
            return message.content or "No final answer was returned."

        if verbose:
            print(
                f"   step {step}: "
                f"{len(message.tool_calls)} tool call(s)"
            )

        # Add the assistant's tool-call message to the conversation.
        messages.append(message)

        # Process EVERY tool call in the response.
        for tool_call in message.tool_calls:

            signature = (
                tool_call.function.name,
                tool_call.function.arguments,
            )

            repeated_calls[signature] += 1

            if repeated_calls[signature] > REPEAT_LIMIT:
                return (
                    "Stopped: the same tool call was repeated "
                    f"{REPEAT_LIMIT} times without progress."
                )

            result = handle_tool_call(tool_call)

            if verbose:
                print(
                    f"      {tool_call.function.name}"
                    f"({tool_call.function.arguments}) -> {result}"
                )

            # One tool message MUST be returned for every tool_call_id.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    return f"Stopped: maximum number of steps ({max_steps}) reached."


if __name__ == "__main__":

    print(
        f"\n=== ROBUST MOVIE AGENT | "
        f"provider: groq | model: {MODEL} ===\n"
    )

    questions = [
        "What is the IMDb rating of Interstellar?",
        "Compare the IMDb ratings of Inception and Dune.",
        "What is the IMDb rating of Interstellar and Inception?",
        "What is the rating of Avatar?",
        "Write a one-line welcome message for movie lovers.",
    ]

    for question in questions:
        print(f"Q: {question}")
        answer = agent(question)
        print(f"A: {answer}\n")