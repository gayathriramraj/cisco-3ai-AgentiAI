"""Demo 3: support agent proposes and (only with confirmation) makes local updates."""
import json
from pathlib import Path
from agent_core import run_agent

PATH = Path(__file__).parent / "data" / "tickets.json"


def get_ticket(ticket_id):
    tickets = json.loads(PATH.read_text(encoding="utf-8"))
    return next((t for t in tickets if t["id"] == ticket_id), None)


def update_ticket_priority(ticket_id, priority):
    if priority not in ("low", "medium", "high"):
        raise ValueError("Invalid priority")
    tickets = json.loads(PATH.read_text(encoding="utf-8"))
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise ValueError("Ticket not found")
    print(f"\nPROPOSED CHANGE: {ticket_id}: {ticket['priority']} -> {priority}")
    permission = input("Apply this local change? Type YES: ").strip()
    if permission != "YES":
        return {"updated": False, "reason": "User declined approval"}
    ticket["priority"] = priority
    PATH.write_text(json.dumps(tickets, indent=2), encoding="utf-8")
    return {"updated": True, "ticket": ticket}

TOOLS = [
    {"type": "function", "function": {"name": "get_ticket", "description": "Read a support ticket by ID", "parameters": {"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]}}},
    {"type": "function", "function": {"name": "update_ticket_priority", "description": "Request permission and then update a support ticket priority", "parameters": {"type": "object", "properties": {"ticket_id": {"type": "string"}, "priority": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["ticket_id", "priority"]}}},
]

if __name__ == "__main__":
    task = input("Ticket instruction (Enter for sample): ").strip() or "Inspect T101 and raise its priority to high if still open."
    print(run_agent(task, TOOLS, {"get_ticket": get_ticket, "update_ticket_priority": update_ticket_priority},
        "You are a helpdesk agent. Inspect ticket first. Only change priority on an open ticket. A separate human approval gate is enforced by the tool."))
