# Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario

For this assessment, I chose a Student Study Planner scenario. The purpose of the scenario is to compare how different reasoning approaches handle study-planning questions that involve both ordinary calculations and information that must be retrieved using a tool.

The study database contains the following study-material information: Python has 20 hours of material, DBMS has 15 hours, and Mathematics has 25 hours. The scenario includes questions that can be solved directly using the information given in the question and a question that requires access to the study database.

The three approaches compared in this assessment are Direct Prompting, Chain-of-Thought (CoT), and a ReAct agent. Self-consistency is also used to observe how repeated Chain-of-Thought runs behave at a non-zero temperature and at temperature 0.

---

## 2. Direct Prompting

Direct prompting asks the language model to answer the user's question immediately without explicitly requesting step-by-step reasoning. In this assessment, the direct-prompting approach does not have access to the study-database tools.

For a reasoning question such as calculating the number of hours remaining after studying Python for a certain number of hours, the model can produce the correct answer directly when all the required information is present in the question. For example, when 3 hours are available each day for 5 days and 2 hours per day are used for Python, the total available time is 15 hours and the Python study time is 10 hours, leaving 5 hours for other subjects.

However, direct prompting cannot retrieve information from the study database because it has no tool access. When asked how many hours of Python study material are available in the database, it correctly states that the information cannot be determined from the information available to it.

The main limitation of direct prompting in this scenario is therefore its lack of external information access. It is suitable for simple questions when all required information is already available in the prompt, but it cannot independently retrieve missing facts.

---

## 3. Chain-of-Thought Prompting

Chain-of-Thought prompting instructs the model to solve a problem step by step before producing the final answer. This approach is useful when a question requires multiple calculations or logical steps.

In the first question of this assessment, the Chain-of-Thought approach calculates the total available study time over five days, calculates the time spent on Python, and subtracts the two values. It therefore reaches the correct answer of 5 hours remaining.

The third question also demonstrates the benefit of step-by-step reasoning. The student has 20 hours of Python material and studies for 3 hours per day for 5 days. The total study time is 15 hours. The completed percentage is therefore (15 / 20) × 100 = 75%.

However, Chain-of-Thought does not automatically provide access to external information. For the question asking for the number of Python study-material hours in the database, the model cannot retrieve the value because the database is not available to the Chain-of-Thought prompt. It therefore correctly identifies that the required information is missing instead of using a tool.

The limitation of Chain-of-Thought in this scenario is that better reasoning cannot compensate for missing external information. The model can reason carefully over information that it already has, but it cannot retrieve information from the study database without a tool.

---

## 4. ReAct Agent

ReAct stands for Reasoning and Acting. Instead of only generating an answer, a ReAct agent can decide that it needs additional information, call a tool, observe the result, and continue reasoning based on that observation.

In this assessment, the ReAct agent has access to two tools: `get_subject_hours()` for retrieving study-material information and `calculator()` for performing calculations.

For the study-planning question, the agent can first call `get_subject_hours("Python")` and receive the observation that Python has 20 hours of study material. It can then use the calculator to determine that studying for 3 hours per day for 5 days gives 15 hours of study time. Finally, it can calculate 15 / 20 × 100 and obtain 75%.

The important difference is that the ReAct agent does not have to invent the missing study-material value. It obtains the value from the tool and then uses that observation in its subsequent reasoning.

The ReAct trace therefore demonstrates the cycle of Thought, Action, and Observation. The thoughts are internal to the model, while the tool actions and their observations are visible in the program output. This makes it possible to observe which tools were called and what information they returned.

The main limitation of ReAct is that it requires additional tool calls and therefore can take more time and computational resources than a direct model response. It is also more complex to implement because the agent must decide when and how to use tools.

---

## 5. Comparison Table

| Basis for comparison | Direct Prompting | Chain-of-Thought | ReAct agent |
|---|---|---|---|
| Reasoning depth | Low; produces an answer directly without explicitly requested reasoning. | Higher; works through a problem step by step. | High; combines reasoning with actions and observations from tools. |
| Tool usage | No tool access in this assessment. | No tool access in this assessment. | Uses tools when external information or calculations are required. |
| Reliability on multi-step questions | Can solve simple multi-step questions, but there is less structured reasoning. | Generally more suitable for multi-step calculations when all required information is available. | Suitable for multi-step problems that require both reasoning and external information. |
| Transparency | The final answer is visible, but no reasoning is shown. | The requested reasoning steps are visible in the response. | Tool actions and observations are visible, making the interaction traceable. |
| Speed / cost | Usually fastest because it requires a single model response. | Usually slower and potentially more expensive because the response contains additional reasoning. | Can be slower and more costly because it may require multiple model calls and tool executions. |
| Consistency across repeated runs | Can vary depending on temperature and prompt. | Can produce different reasoning paths at non-zero temperature. | Can also vary in its tool-use path, depending on the model and temperature. |

---

## 6. Self-Consistency Observation

Self-consistency was tested using the Chain-of-Thought question about completing Python study material. The question contained 20 hours of material, and the student studied for 3 hours per day for 5 days. The correct result is 75%.

The experiment was run five times with a non-zero temperature of 0.8. The repeated responses produced the correct underlying answer of 75%, although the wording and formatting of the answers could vary between runs. This demonstrates that non-zero temperature can allow variation between repeated generations even when the underlying problem and correct answer remain the same.

The same experiment was then run five times with temperature set to 0. In this experiment, all five runs produced the same 75% answer and essentially the same response. This shows that, for this configuration, temperature 0 produced a deterministic response across the repeated runs.

Self-consistency can therefore be useful when multiple reasoning paths are generated at a non-zero temperature and the most frequently occurring answer is selected. However, repeated answers are not automatically proof of correctness; the underlying problem and reasoning still need to be evaluated.

---

## 7. Suitability Analysis

For the Student Study Planner scenario, the ReAct approach is suitable when the question requires information from the study database as well as calculations. Direct prompting and Chain-of-Thought can solve questions when all necessary information is already provided, but they cannot independently retrieve the missing study-material hours.

The ReAct agent can obtain the Python study-material value using `get_subject_hours()` and then use the calculator to perform the required calculations. This makes the approach appropriate for the part of the scenario where external information is required.

The comparison also shows that Chain-of-Thought is useful for multi-step reasoning when the necessary information is already available. Direct prompting is sufficient for simple questions where a short direct response is enough. Therefore, the appropriate approach depends on the type of problem rather than one approach being suitable for every situation.

The self-consistency experiment also shows that repeated Chain-of-Thought generations can vary at a non-zero temperature. In this experiment, the repeated answers still produced the correct underlying result of 75%, while temperature 0 produced the same response across all five runs.

---

## 8. Conclusion

Direct prompting is appropriate for simple questions and tasks where the required information is already available and a direct response is sufficient. It is generally the simplest and fastest approach, but it does not provide tool-based access to missing information.

Chain-of-Thought is appropriate for problems that require several reasoning or calculation steps. It can make the reasoning process more structured and can help with multi-step problems, but it still depends on the information available to the model and cannot retrieve external facts without tools.

ReAct is appropriate for problems that combine reasoning with interaction with external tools or information sources. It can reason about what information is required, perform an action such as calling a tool, observe the result, and continue until it can produce a final answer. This makes it useful for tasks where the model's existing knowledge is not sufficient.

The Student Study Planner scenario demonstrates the difference clearly. Direct Prompting and Chain-of-Thought can reason over information already supplied, while ReAct can additionally obtain information from a tool and use that information during the reasoning process.