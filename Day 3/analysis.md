# Day 3 – Building an Agent Loop from Scratch

## Objective

The objective of Day 3 was to understand how an agent loop works internally without relying on an agent framework.

The agent consists of:
- System prompt
- Message list
- Tool registry
- Tool schemas
- Agent loop
- Stopping conditions

## Agent Loop

The agent follows this basic process:

1. Send the conversation and available tools to the LLM.
2. Check whether the LLM requested a tool.
3. If no tool is requested, stop and return the final answer.
4. Record the assistant's tool request.
5. Execute the requested tool.
6. Add the tool result back to the conversation.
7. Continue the loop until a final answer or safety condition is reached.

## Tools Used

### Calculator

The calculator evaluates basic arithmetic expressions safely.

### read_webpage

The `read_webpage` tool can read:
- HTTP/HTTPS webpages
- Local HTML/text files

It also limits the amount of text returned to prevent excessive context.

## Normal Agent Test

The agent read `notice.html` and then used the calculator.

Tool sequence:

read_webpage("notice.html")
→ fee information retrieved

calculator("30000*0.9")
→ 27000.0

Final answer: ₹27,000.

## Error Handling Test

The agent was asked to read `fees.html`, which does not exist.

The tool returned an error instead of crashing:

"Read error: 'fees.html' is not a URL and no such file exists."

The agent then returned a message explaining that the file could not be located.

## Guarded Agent

The fixed version contains three guards:

1. Repeat-call detection
2. Maximum observation size
3. Total character budget

### Repeat-call Detection

When the agent repeatedly called:

read_webpage("big.html")

with the same arguments and no progress, the agent stopped after the configured limit and returned:

"Stopped: the tool read_webpage was called 3 times with the same arguments and no progress was made."

This prevents the agent from getting stuck in a repeated tool-call loop.

## Key Learning

Day 3 showed that an agent is not simply an LLM response. The agent loop coordinates the LLM, tools, tool results, conversation state, and stopping conditions.

Safety conditions are important because agents can encounter repeated tool calls, excessive tool output, context growth, tool errors, or other failure modes.

## Conclusion

In Day 3, I built and tested a ReAct-style agent loop from scratch. The agent successfully used multiple tools, handled a missing-file error, and stopped a repeated tool call using a safety guard.