"""Demo 4: an agent reads business data, computes metrics and writes a local report."""
import csv
from collections import defaultdict
from pathlib import Path
from agent_core import run_agent

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "sales.csv"
OUT = ROOT / "output" / "sales_report.md"


def summarize_sales():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    monthly = defaultdict(float)
    region = defaultdict(float)
    for r in rows:
        monthly[r["month"]] += float(r["revenue"])
        region[r["region"]] += float(r["revenue"])
    return {"total_revenue": sum(monthly.values()), "monthly_revenue": dict(monthly), "regional_revenue": dict(region)}


def save_report(title, report_markdown):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Fixed destination prevents arbitrary model-directed file writes.
    OUT.write_text(f"# {title}\n\n{report_markdown}\n", encoding="utf-8")
    return {"saved": True, "path": str(OUT)}

TOOLS = [
    {"type": "function", "function": {"name": "summarize_sales", "description": "Compute exact revenue totals from sales.csv", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "save_report", "description": "Save a Markdown sales report to the fixed local output path", "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "report_markdown": {"type": "string"}}, "required": ["title", "report_markdown"]}}},
]

if __name__ == "__main__":
    task = "Read sales data, compute monthly and regional revenue, identify the best-performing month, then save a short factual report."
    print(run_agent(task, TOOLS, {"summarize_sales": summarize_sales, "save_report": save_report},
        "You are a sales reporting agent. First call summarize_sales, then save_report. Use only computed figures. Never invent data."))
    print(f"Check report: {OUT}")
