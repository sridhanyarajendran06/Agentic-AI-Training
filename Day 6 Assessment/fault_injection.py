"""Fault injection tests for the Day 6 assessment."""

import json

from robust_agent import handle_tool_call


class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class FakeToolCall:
    def __init__(self, name, arguments, call_id):
        self.id = call_id
        self.function = FakeFunction(name, arguments)


FAULTS = [
    (
        "1. Invalid JSON",
        FakeToolCall(
            "get_movie_rating",
            '{"movie": "Interstellar",',
            "fault-1",
        ),
    ),
    (
        "2. Unknown tool",
        FakeToolCall(
            "get_weather",
            '{"city": "Chennai"}',
            "fault-2",
        ),
    ),
    (
        "3. Missing required argument",
        FakeToolCall(
            "get_movie_rating",
            json.dumps({"movie": "Interstellar"}),
            "fault-3",
        ),
    ),
    (
        "4. Wrong argument type",
        FakeToolCall(
            "calculate_watch_score",
            json.dumps({
                "rating": "8.7",
                "hours_available": 3,
            }),
            "fault-4",
        ),
    ),
    (
        "5. Invalid enum value",
        FakeToolCall(
            "get_movie_rating",
            json.dumps({
                "movie": "Interstellar",
                "platform": "Netflix",
            }),
            "fault-5",
        ),
    ),
    (
        "6. Invented extra argument",
        FakeToolCall(
            "get_movie_rating",
            json.dumps({
                "movie": "Interstellar",
                "platform": "IMDb",
                "year": 2014,
            }),
            "fault-6",
        ),
    ),
    (
        "7. Unknown movie",
        FakeToolCall(
            "get_movie_rating",
            json.dumps({
                "movie": "Avatar",
                "platform": "IMDb",
            }),
            "fault-7",
        ),
    ),
    (
        "8. Invalid calculation value",
        FakeToolCall(
            "calculate_watch_score",
            json.dumps({
                "rating": 8.5,
                "hours_available": 0,
            }),
            "fault-8",
        ),
    ),
    (
        "9. Empty arguments",
        FakeToolCall(
            "get_movie_rating",
            "",
            "fault-9",
        ),
    ),
    (
        "10. Negative hours",
        FakeToolCall(
            "calculate_watch_score",
            json.dumps({
                "rating": 8.5,
                "hours_available": -2,
            }),
            "fault-10",
        ),
    ),
]


if __name__ == "__main__":

    print("\n=== FAULT INJECTION TESTS ===\n")

    for name, tool_call in FAULTS:
        result = handle_tool_call(tool_call, log=False)

        print(name)
        print(f"Result: {result}")
        print(f"Returned type: {type(result).__name__}")
        print("-" * 70)