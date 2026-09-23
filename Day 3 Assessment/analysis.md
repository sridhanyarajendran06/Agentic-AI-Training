# Day 3 Assessment – From Prompt to Action

## Scenario

For this assessment, I chose a Student Study Planner scenario.

The scenario contains a private study database with the following information:

| Subject | Available Study Material |
|---|---:|
| Python | 20 hours |
| DBMS | 15 hours |
| Mathematics | 25 hours |

The purpose of the experiment is to compare a plain LLM prompt with the same LLM when it has access to one external tool: `get_subject_hours()`.

The tool can retrieve information from the private study database that is not provided directly in the prompt.

---

# 1. Explanation of Concepts

## What is a Large Language Model?

A Large Language Model (LLM) is a model trained on large amounts of text that can understand prompts and generate natural-language responses.

In this scenario, the plain LLM was able to answer questions that could be handled using its existing knowledge or simple reasoning. For example, when asked:

> If I study 3 hours per day for 5 days, how many hours will I study in total?

The LLM correctly calculated:

3 × 5 = 15 hours.

It also correctly answered that the capital of France is Paris.

However, when asked:

> How many hours of Python study material are available in my study database?

the plain LLM correctly stated that it did not have access to the personal study database. It did not have a way to retrieve the private value of 20 hours.

This shows an important limitation: an LLM can generate an answer from its learned knowledge and reasoning ability, but it does not automatically have access to a private database or external information source.

---

## What is an Agent?

An agent is an LLM-based system that can use available tools to perform actions or obtain information before producing its final answer.

A plain chat response directly generates an answer from the information available to the model.

An agent can instead follow a process such as:

1. Receive the user's question.
2. Determine whether additional information is required.
3. Select an appropriate tool.
4. Call the tool with the required parameters.
5. Receive the tool result.
6. Use the result to produce the final answer.

In this assessment, the tool-enabled system behaved differently from the plain LLM when the question required information from the private study database.

For the Python study-material question, the agent called:

`get_subject_hours("Python")`

The tool returned:

`20`

The model then used this result to produce the final answer that the database contains 20 hours of Python material.

---

## What is a Tool and What is a Tool Call?

A tool is an external function that an LLM can use to obtain information or perform an operation that it cannot reliably perform from its own knowledge alone.

In this assessment, the tool was:

`get_subject_hours(subject)`

The tool accesses the private study-hour data.

A tool call is the request made by the model to execute a particular tool with specific arguments.

For example:

```text
TOOL CALL: get_subject_hours {"subject":"Python"}