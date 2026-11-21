"""Demo 2: agent chooses inventory lookup functions over CSV data."""
import csv
from pathlib import Path
from agent_core import run_agent

DATA = Path(__file__).parent / "data" / "inventory.csv"


def inventory_rows():
    with DATA.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def list_inventory():
    return inventory_rows()


def low_stock_items():
    return [r for r in inventory_rows() if int(r["quantity"]) < int(r["reorder_level"])]


def lookup_product(sku):
    return next((r for r in inventory_rows() if r["sku"].upper() == sku.upper()), None)


def tool(name, description, properties=None, required=None):
    return {"type": "function", "function": {"name": name, "description": description,
        "parameters": {"type": "object", "properties": properties or {}, "required": required or []}}}

TOOLS = [
    tool("list_inventory", "Get all inventory records"),
    tool("low_stock_items", "Get products whose quantity is below reorder level"),
    tool("lookup_product", "Find inventory product by SKU", {"sku": {"type": "string"}}, ["sku"]),
]

if __name__ == "__main__":
    task = input("Inventory question (Enter for sample): ").strip() or "Which products need reordering and what are their stock levels?"
    functions = {"list_inventory": list_inventory, "low_stock_items": low_stock_items, "lookup_product": lookup_product}
    print(run_agent(task, TOOLS, functions, "You are an inventory assistant. Base answers strictly on tool results. Do not invent quantities."))
