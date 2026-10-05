"""Tools and JSON schemas for the Day 6 assessment."""

MOVIE_RATINGS = {
    "Interstellar": {
        "IMDb": 8.7,
        "Rotten Tomatoes": 73,
    },
    "Inception": {
        "IMDb": 8.8,
        "Rotten Tomatoes": 87,
    },
    "Dune": {
        "IMDb": 8.0,
        "Rotten Tomatoes": 83,
    },
}


def get_movie_rating(movie, platform):
    """Return the rating of a movie from the requested platform."""

    if movie not in MOVIE_RATINGS:
        return f"No rating data found for {movie}."

    if platform not in MOVIE_RATINGS[movie]:
        return f"No rating available from {platform} for {movie}."

    return str(MOVIE_RATINGS[movie][platform])


def calculate_watch_score(rating, hours_available):
    """Calculate a simple watch score."""

    if hours_available <= 0:
        return "Hours available must be greater than zero."

    score = rating * min(hours_available / 3, 1)
    return round(score, 2)


# Single schema dictionary used by BOTH the model and the validator.
SCHEMAS = {
    "get_movie_rating": {
        "type": "function",
        "function": {
            "name": "get_movie_rating",
            "description": "Look up a movie rating from a specific rating platform.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "movie": {
                        "type": "string",
                        "description": "The movie title.",
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["IMDb", "Rotten Tomatoes"],
                        "description": "The rating platform.",
                    },
                },
                "required": ["movie", "platform"],
                "additionalProperties": False,
            },
        },
    },
    "calculate_watch_score": {
        "type": "function",
        "function": {
            "name": "calculate_watch_score",
            "description": "Calculate a watch score using a movie rating and available hours.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "rating": {
                        "type": "number",
                        "description": "Movie rating.",
                    },
                    "hours_available": {
                        "type": "number",
                        "description": "Number of hours available for watching.",
                    },
                },
                "required": ["rating", "hours_available"],
                "additionalProperties": False,
            },
        },
    },
}


TOOL_FUNCTIONS = {
    "get_movie_rating": get_movie_rating,
    "calculate_watch_score": calculate_watch_score,
}