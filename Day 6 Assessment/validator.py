"""Schema validator for the Day 6 assessment."""

from tools import SCHEMAS


def validate_arguments(tool_name, arguments):
    """Validate tool arguments against the tool's JSON schema.

    Returns:
        None if valid.
        A descriptive error message if invalid.
    """

    if tool_name not in SCHEMAS:
        return f"Unknown tool: {tool_name}"

    schema = SCHEMAS[tool_name]["function"]["parameters"]

    if not isinstance(arguments, dict):
        return "Invalid arguments: expected a JSON object."

    properties = schema["properties"]
    required = schema["required"]

    # 1. Check missing required arguments
    for field in required:
        if field not in arguments:
            return (
                f"Missing required argument '{field}'. "
                f"Expected required fields: {required}."
            )

    # 2. Check invented / extra arguments
    if schema.get("additionalProperties") is False:
        extra_fields = set(arguments) - set(properties)

        if extra_fields:
            return (
                f"Invented argument(s): {sorted(extra_fields)}. "
                f"Expected only: {list(properties)}."
            )

    # 3. Check argument types
    for field, value in arguments.items():
        expected_type = properties[field]["type"]

        if expected_type == "string" and not isinstance(value, str):
            return (
                f"Wrong type for '{field}': expected string, "
                f"got {type(value).__name__}."
            )

        if expected_type == "number" and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            return (
                f"Wrong type for '{field}': expected number, "
                f"got {type(value).__name__}."
            )

    # 4. Check enum values
    for field, value in arguments.items():
        if "enum" in properties[field]:
            allowed_values = properties[field]["enum"]

            if value not in allowed_values:
                return (
                    f"Invalid value for '{field}': '{value}'. "
                    f"Expected one of: {allowed_values}."
                )

    return None


if __name__ == "__main__":
    tests = [
        (
            "Valid call",
            "get_movie_rating",
            {
                "movie": "Interstellar",
                "platform": "IMDb",
            },
        ),
        (
            "Missing required argument",
            "get_movie_rating",
            {
                "movie": "Interstellar",
            },
        ),
        (
            "Invented extra argument",
            "get_movie_rating",
            {
                "movie": "Interstellar",
                "platform": "IMDb",
                "year": 2014,
            },
        ),
        (
            "Wrong type",
            "calculate_watch_score",
            {
                "rating": "8.7",
                "hours_available": 3,
            },
        ),
        (
            "Invalid enum",
            "get_movie_rating",
            {
                "movie": "Interstellar",
                "platform": "Netflix",
            },
        ),
    ]

    print("\n=== VALIDATOR TESTS ===\n")

    for name, tool_name, arguments in tests:
        result = validate_arguments(tool_name, arguments)

        if result is None:
            print(f"{name}: VALID")
        else:
            print(f"{name}: {result}")