# Day 6 Assessment
# Reliable Tool Calling: Schemas, Validation, Retry and Structured Outputs

## 1. Scenario

### Movie Recommendation Assistant

For this assessment, I created a simple Movie Recommendation Assistant.

The assistant has two tools:

1. `get_movie_rating`
   - Looks up a movie rating from IMDb or Rotten Tomatoes.
2. `calculate_watch_score`
   - Calculates a simple watch score using a movie rating and the number of hours available.

The movie data used in the scenario is:

| Movie | IMDb | Rotten Tomatoes |
|---|---:|---:|
| Interstellar | 8.7 | 73 |
| Inception | 8.8 | 87 |
| Dune | 8.0 | 83 |

The purpose of this scenario is not to build a large application, but to demonstrate reliable tool calling, validation, structured outputs and fault handling.

---

# 2. Explanation of Concepts

## 2.1 What is the Chat Completions format?

The Chat Completions API sends a request containing messages and, when required, tools.

The main request fields used in my implementation are:

- `model` – the model being used.
- `messages` – the conversation history.
- `tools` – the available tool definitions.
- `tool_choice` – controls whether the model can or must use a tool.
- `max_tokens` – limits the generated output.

A response contains choices. Each choice contains a message and a `finish_reason`.

The important `finish_reason` values are:

### `stop`

The model has finished generating its response.

My agent checks whether there are tool calls. If there are none, the response is treated as the final answer.

### `length`

The response was stopped because it reached the token limit.

My agent does not immediately fail. It retries the request with a larger `max_tokens` value.

### `tool_calls`

The model wants my program to execute one or more tools.

The model does not execute the Python function itself. My code receives the tool call, validates it and executes the corresponding Python function.

`message.content` can be empty when the model wants a tool because the useful output is contained in `message.tool_calls` instead of normal text content.

For example, the model can request:

```text
get_movie_rating(
    movie="Interstellar",
    platform="IMDb"
)