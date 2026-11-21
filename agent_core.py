
"""
Agentic AI - Common Agent Core
Uses Groq API with local Python function calling.

Shows:
1. User question
2. AI model decision
3. Selected tool
4. Tool arguments
5. Python function execution
6. Tool result
7. Final AI response
"""

import json
import os

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------
# STEP 1: Load environment variables
# ---------------------------------------

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


# ---------------------------------------
# STEP 2: Define the agent
# ---------------------------------------

def run_agent(
    task,
    tools,
    functions,
    instructions,
    max_steps=5
):

    # Create Groq client
    client = Groq()

    # Prepare messages for the AI model
    messages = [
        {
            "role": "system",
            "content": (
                instructions
                + "\nUse tools when needed."
                + "\nBase answers on actual tool results."
                + "\nNever claim an action was completed "
                  "unless a tool confirms it."
            )
        },
        {
            "role": "user",
            "content": task
        }
    ]

    print("\n================================")
    print("AGENT STARTED")
    print("================================")

    print("Model:", MODEL)
    print("User Question:", task)

    print("\nAvailable Tools:")

    for tool in tools:
        print("-", tool["function"]["name"])

    # ---------------------------------------
    # STEP 3: Start agent execution loop
    # ---------------------------------------

    for step in range(max_steps):

        print("\n================================")
        print(f"AGENT STEP {step + 1}")
        print("================================")

        # Require a tool on the first step for
        # classroom demonstration.
        # Subsequent steps allow the AI to
        # choose tools or produce a final answer.

        choice = "required" if step == 0 else "auto"

        print("Tool Choice:", choice)

        # -----------------------------------
        # STEP 4: Call Groq AI model
        # -----------------------------------

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice=choice,
            temperature=0
        )

        # Get the AI message
        message = response.choices[0].message

        print("\n----- AI MODEL RESPONSE -----")

        print("AI Content:", message.content)

        print("Tool Calls:", message.tool_calls)

        # -----------------------------------
        # STEP 5: Check if AI requested tools
        # -----------------------------------

        if not message.tool_calls:

            print("\nNo additional tool requested.")

            final_answer = (
                message.content or "(No text returned)"
            )

            print("\n================================")
            print("AGENT COMPLETED")
            print("================================")

            return final_answer

        # Store AI tool request in history
        messages.append(
            message.model_dump(exclude_none=True)
        )

        # -----------------------------------
        # STEP 6: Execute requested tools
        # -----------------------------------

        for call in message.tool_calls:

            name = call.function.name

            print("\n----- TOOL SELECTED -----")

            print("Tool Name:", name)

            print(
                "Tool Arguments:",
                call.function.arguments
            )

            try:

                # Convert JSON arguments to dict
                args = json.loads(
                    call.function.arguments
                )

                # Verify requested tool is allowed
                if name not in functions:
                    raise ValueError(
                        f"Tool not allowed: {name}"
                    )

                # Verify arguments are an object
                if not isinstance(args, dict):
                    raise ValueError(
                        "Tool arguments must be a JSON object"
                    )

                print("\nExecuting Python function...")

                # Execute actual Python function
                output = functions[name](**args)

                print("Python function executed.")

                # Convert result to JSON
                result = json.dumps(
                    {
                        "ok": True,
                        "result": output
                    },
                    default=str
                )

            except Exception as exc:

                print("Tool Execution Error:", str(exc))

                result = json.dumps(
                    {
                        "ok": False,
                        "error": str(exc)
                    }
                )

            # -----------------------------------
            # STEP 7: Print tool result
            # -----------------------------------

            print("\n----- TOOL RESULT -----")

            print(result[:1000])

            # Add tool result to AI conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": name,
                    "content": result
                }
            )

        print("\nTool result added to AI messages.")
        print("Agent will continue to next step.")

    # ---------------------------------------
    # STEP 8: Maximum iteration handling
    # ---------------------------------------

    print("\nMaximum agent steps reached.")

    return (
        "Stopped at maximum tool-call rounds. "
        "Review the execution trace above."
    )
