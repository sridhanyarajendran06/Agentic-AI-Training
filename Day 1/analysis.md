# Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## 1. Introduction

This project compares three approaches for solving a small private-data problem: a plain chatbot, a rule-based workflow, and a tool-using AI agent. The chosen scenario is a course fee information system containing private course-fee data.

The private course data used in this project is:

| Course Code | Course Fee |
|-------------|------------|
| CS101       | ₹12,000    |
| AI202       | ₹18,000    |
| DS303       | ₹15,000    |

The same course-fee scenario is given to all three systems. The purpose is to understand how their capabilities differ when answering questions involving private data, fixed rules, calculations, and multi-step reasoning.

The three systems represent three different approaches. The plain chatbot mainly uses an LLM to generate responses without access to the private course-fee data. The rule-based workflow uses predefined rules and conditions to process specific questions without an LLM. The AI agent combines an LLM with tools and a loop so that it can decide which tools to use, observe their results, and continue until it can produce an answer.

---

# 2. System 1: Plain Chatbot

## 2.1 How it works

The plain chatbot uses an LLM to generate responses to user questions. It does not use the private course-fee data and does not use external tools or predefined business rules for retrieving course fees.

The user provides a question, which is sent to the LLM. The LLM generates a response based on the information available to it. Since the private course-fee values are not provided to the chatbot as a tool or data source, it cannot reliably answer questions that require those values.

For example, when asked for the fee of AI202, the chatbot does not provide the private value of ₹18,000. Instead, it explains that it does not have the specific fee information and asks for additional information.

Similarly, when asked to calculate the total fee for CS101 and AI202 after a 10% scholarship, the chatbot cannot perform the calculation using the private course values because it does not have access to those values.

## 2.2 Data and tools

The plain chatbot uses the LLM as its main component. It does not use the private course-fee dictionary, course-fee tools, or calculator tools.

Therefore, it has no direct access to the private course data in this project.

## 2.3 Limitations

The main limitation of the plain chatbot in this scenario is its lack of access to the private data. It can answer general questions, such as writing a welcome message for new AI students, but it cannot reliably answer questions that depend on the private course-fee values.

This demonstrates that an LLM alone is not sufficient when accurate answers depend on information that is stored privately and has not been provided to the model.

---

# 3. System 2: Rule-Based Workflow

## 3.1 How it works

The rule-based workflow does not use an LLM. Instead, it uses predefined rules and conditions written in the program.

The workflow checks the user's question for expected patterns and then performs the corresponding predefined action. For example, a rule can recognize a question about the fee of AI202 and return the stored value of ₹18,000.

The workflow can also perform predefined calculations. For example, for the question asking for the total fee of CS101 and AI202 after a 10% scholarship, it can retrieve the two known fees and calculate the discounted total.

## 3.2 Data and tools

The workflow has access to the private course-fee information through predefined program data.

However, it does not use an LLM or dynamically select tools. Its behavior is determined by the rules that were explicitly written by the developer.

## 3.3 Limitations

The main limitation of the rule-based workflow is that it is rigid. It works well when the user's question matches a predefined rule, but it may fail when the question is phrased differently or when the user asks a type of question for which no rule exists.

For example, the workflow can answer specific course-fee questions for which rules were created, but it does not automatically reason about a new budget-based question such as:

"I can pay Rs. 30,000. Which two courses can I take together within this budget?"

The workflow does not dynamically decide which course-fee information to retrieve or which calculations to perform unless those rules have already been programmed.

---

# 4. System 3: AI Agent

## 4.1 How it works

The AI agent combines three main components:

**Agent = LLM + Tools + Loop**

The LLM understands the user's question and decides what action is required. Tools provide access to the private course-fee information and perform calculations. The loop allows the agent to continue working after receiving the result of a tool call.

The agent in this project uses two main tools:

1. `get_course_fee(course_code)` - retrieves the fee of a specific course.
2. `calculator(expression)` - performs arithmetic calculations safely.

For example, when asked:

"Is DS303 more expensive than CS101, and by how much?"

the agent performs multiple steps:

1. It calls `get_course_fee` for DS303.
2. It calls `get_course_fee` for CS101.
3. It sends the difference calculation to the calculator tool.
4. It observes the result of ₹3,000.
5. It produces the final answer.

This demonstrates the tool-using loop of an AI agent.

## 4.2 Data and tools

Unlike the plain chatbot, the AI agent has controlled access to the private course-fee data through the `get_course_fee` tool.

It also has access to the calculator tool for arithmetic operations.

The agent does not need a separate hard-coded rule for every possible wording of a question. Instead, the LLM can interpret the request and decide which available tools are necessary.

## 4.3 Limitations

The AI agent is more flexible than the rule-based workflow, but its behavior depends on the LLM correctly understanding the task and selecting the appropriate tools.

Therefore, an agent can be less predictable than a strictly predefined workflow. Tool errors, model limitations, incorrect tool selection, or API limitations can affect its execution.

However, within this project, the agent successfully handled multi-step course-fee questions by retrieving private data and performing calculations using its tools.

---

# 5. Comparison of the Three Approaches

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|-----------------------|----------------|----------------------|----------|
| Flexibility | High for general conversation, but limited by available knowledge and no private-data access | Low to moderate because behavior depends on predefined rules | High because the LLM can interpret different requests and select tools |
| Decision-making | Generates a response but does not dynamically select tools | Follows predefined conditions and actions | LLM decides which tools and actions are required |
| Tool usage | No tools in this implementation | Uses predefined program logic rather than LLM-selected tools | Uses tools such as `get_course_fee` and `calculator` |
| Private-data access | No direct access to the private course-fee data | Yes, through predefined program data and rules | Yes, through controlled tools |
| Multi-step task handling | Limited for private-data tasks | Possible only when the required sequence is explicitly programmed | Can perform multiple tool calls and continue through a reasoning loop |
| Automation | Suitable for conversational responses | High for predictable and fixed processes | High for dynamic multi-step tasks |
| Reliability | Good for general language generation, but unreliable for unavailable private facts | High for cases covered by predefined rules | Can be effective for complex tasks, but depends on model and tool selection |

The comparison shows that the three approaches make different trade-offs. The plain chatbot is simple and useful for general conversational tasks but cannot directly access the private data used in this scenario. The rule-based workflow provides predictable behavior for known cases but becomes rigid when new types of questions are introduced. The AI agent provides more flexibility because it can interpret the request, select tools, use their results, and continue with additional actions.

---

# 6. Suitability Analysis

For the chosen private course-fee scenario, the AI agent is the most suitable approach when the requirement includes answering different types of questions involving private data and performing multi-step calculations.

The main reason is that the agent can combine access to private data with dynamic decision-making. It can retrieve individual course fees using `get_course_fee` and use the calculator when arithmetic is required. This allows it to handle questions that require multiple steps without requiring a separate hard-coded rule for every possible question structure.

The rule-based workflow is suitable when the questions and required operations are known in advance and predictable behavior is important. It can provide consistent results for the cases covered by its rules, but adding new question types requires additional rules.

The plain chatbot is suitable for general conversational requests that do not require access to the private course-fee information. In this project, it successfully handles a general request such as generating a welcome message, but it cannot reliably answer the private-data questions.

Therefore, the choice depends on the task requirements. For this scenario, where users may ask varied questions involving private data and calculations, the tool-using AI agent provides the required combination of flexibility, private-data access, and multi-step task handling.

---

# 7. Challenge Question

The project also includes an additional challenge question:

"I can pay Rs. 30,000. Which two courses can I take together within this budget?"

This question was not directly covered by the predefined workflow rules. Therefore, the rule-based workflow does not automatically have a rule for solving this type of budget-selection problem.

The AI agent can approach this question differently because it can use the available course-fee tool to obtain the required values and reason about combinations of courses.

For example:

- CS101 + AI202 = ₹30,000
- CS101 + DS303 = ₹27,000
- AI202 + DS303 = ₹33,000

Therefore, the first two combinations are within a ₹30,000 budget.

This challenge demonstrates the difference between a fixed workflow and a tool-using agent when a question is not explicitly represented by a predefined rule.

---

# 8. Conclusion

A plain chatbot, a rule-based workflow, and an AI agent are different approaches for solving problems.

A plain chatbot is appropriate when the main requirement is natural-language conversation, explanation, or generation and the task does not require access to private information or external tools.

A rule-based workflow is appropriate when the process is predictable, the conditions are clearly known, and consistent predefined behavior is more important than flexibility. It is useful for tasks where the same steps must be followed every time.

An AI agent is appropriate when a task is dynamic, requires access to tools or private data, and may involve multiple steps. The agent can use an LLM to understand the request, select appropriate tools, observe their results, and continue until the task is completed.

The key difference demonstrated by this project can therefore be summarized as:

**Plain chatbot = LLM**

**Rule-based workflow = predefined rules and conditions**

**AI agent = LLM + Tools + Loop**

The choice between these approaches should depend on the requirements of the problem, including the need for flexibility, private-data access, predictable behavior, tool usage, and multi-step task handling.