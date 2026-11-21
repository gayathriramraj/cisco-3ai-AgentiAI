"""Demo 1: model decides when to call a calculator."""
from agent_core import run_agent


def calculate(operation, a, b):
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    raise ValueError("Unknown operation")

TOOLS = [{"type": "function", "function": {
    "name": "calculate", "description": "Perform exact arithmetic on two numbers.",
    "parameters": {"type": "object", "properties": {
        "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
        "a": {"type": "number"}, "b": {"type": "number"}
    }, "required": ["operation", "a", "b"]}
}}]

if __name__ == "__main__":
    task = input("Ask a calculation (Enter for sample): ").strip() or "What is 18% GST on 1250 rupees? Give tax and total."
    print(run_agent(task, TOOLS, {"calculate": calculate}, "You are a helpful calculator agent. Use the calculator for arithmetic."))
