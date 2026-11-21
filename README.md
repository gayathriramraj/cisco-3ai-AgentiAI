# Five beginner Agentic AI labs (Python + Groq)

## Setup
1. Install Python 3.10+ and VS Code.
2. Open this folder in VS Code terminal.
3. Create virtual environment:
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install: `python -m pip install -r requirements.txt`
5. Copy `.env.example` to `.env`. Replace the placeholder with your own Groq API key. Never commit `.env`.
6. Run each demo: `python demo_01_calculator.py` etc. If your account has a different supported model, adjust `GROQ_MODEL` in `.env`.

## Demo 1 — Calculator tool agent (15–20 min)
- Run `python demo_01_calculator.py`.
- Enter: `What is 18% GST on 1250 rupees? Give tax and total.`
- Watch `[Tool call] calculate` and `[Tool result]`; verify ₹225 tax and ₹1475 total.
- Change prompt to `What is 250 divided by 0?` and discuss error handling.
- Concept: model selects tool, Python executes, result returns to model.

## Demo 2 — Inventory lookup agent (20 min)
- Open `data/inventory.csv`. Identify fields and reorder thresholds.
- Run `python demo_02_inventory.py`.
- Ask: `Which products must be reordered?`
- Expected: Laptop P001, Keyboard P003, USB Cable P005.
- Ask `What is the quantity of P002?` and inspect selected tool.
- Concept: grounded answers from a real data source, not invented stock numbers.

## Demo 3 — Helpdesk update with approval (20 min)
- Open `data/tickets.json`. Inspect T101 status and priority.
- Run `python demo_03_ticket_agent.py`.
- Enter sample request (or press Enter). The agent reads T101 and requests a priority change.
- Type anything other than `YES` to decline; check file unchanged.
- Run again, type `YES`, and check file modified.
- Concept: read vs write permissions, human-in-the-loop approval, audit trace.
- To reset: edit T101 priority in JSON back to `medium`.

## Demo 4 — Sales reporting agent (20–25 min)
- Open `data/sales.csv`.
- Run `python demo_04_report_agent.py`.
- Watch `summarize_sales` then `save_report` tool calls.
- Inspect `output/sales_report.md`.
- Verify January=267500, February=225000, March=372500, total=865000. March highest.
- Concept: plan -> tool -> result -> persisted artifact; grounded arithmetic.

## Demo 5 — Writer/reviewer multi-agent (20–25 min)
- Run `python demo_05_multi_agent.py`.
- Enter: `Explain password safety to first-year students`.
- Observe agent 1 draft, agent 2 critique and agent 1 revision.
- Modify reviewer to flag confusing technical language and compare final version.
- Concept: specialized roles, review feedback, bounded revision loop.

## Training flow (2 hours)
- 10 min: What makes an agent different from a simple chatbot?
- 20 min: Demo 1
- 20 min: Demo 2
- 20 min: Demo 3
- 25 min: Demo 4
- 20 min: Demo 5
- 5 min: Exit quiz: agent, tool, observation, guardrail, multi-agent.

## Notes
- Requires a working Groq API key, internet access, and an available tool-capable model. Rate limits and pricing depend on your account.
- An LLM chooses tools, but Python actually executes them; tools do not run merely because the model mentions them.
- `run_agent` limits tool-call rounds to 5 and restricts functions to an allowlist.
- Demo 3 requires explicit approval for the write. Demo 4 uses a fixed local output file.
- The multi-agent example uses sequential roles, not autonomous networked agents.
