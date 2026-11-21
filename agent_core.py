"""Shared bounded local-tool agent loop for training demonstrations."""
import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def ask_llm(system, user):
    client = Groq()
    result = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0,
    )
    return result.choices[0].message.content or ""


def run_agent(task, tools, functions, instructions, max_steps=5):
    """The model requests local tools; Python executes only explicitly allowed tools."""
    client = Groq()
    messages = [
        {"role": "system", "content": instructions + "\nUse tools when needed. Never claim an action was completed unless a tool confirms it."},
        {"role": "user", "content": task},
    ]
    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools, tool_choice="auto", temperature=0
        )
        message = response.choices[0].message
        if not message.tool_calls:
            return message.content or "(No text returned)"
        messages.append(message.model_dump(exclude_none=True))
        for call in message.tool_calls:
            name = call.function.name
            print(f"[Tool call {step + 1}] {name}: {call.function.arguments}")
            try:
                args = json.loads(call.function.arguments)
                if name not in functions:
                    raise ValueError(f"Tool not allowed: {name}")
                output = functions[name](**args)
                result = json.dumps({"ok": True, "result": output}, default=str)
            except Exception as exc:
                result = json.dumps({"ok": False, "error": str(exc)})
            print(f"[Tool result] {result[:500]}")
            messages.append({
                "role": "tool", "tool_call_id": call.id, "name": name, "content": result
            })
    # Do not let final response falsely claim a tool ran after hitting limit.
    return "Stopped at the maximum tool-call rounds. Review the trace above."
