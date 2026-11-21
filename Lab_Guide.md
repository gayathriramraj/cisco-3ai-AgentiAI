# Agentic AI: Five Hands-on Python Labs

**Participant Lab Guide**  
**Level:** Beginner  
**Estimated duration:** 2 hours (including setup and recap)  
**Tools:** Python 3.10+, VS Code, Groq API, terminal

> **Before class:** Obtain the trainer's companion lab code package. This guide references Python files and datasets from that package; the Markdown document by itself does not contain those runnable files.

## Learning outcomes

By the end of the session, you should be able to:

1. Explain how a tool-using AI agent differs from a standard chatbot.
2. Identify the user request, agent, tool call, tool response and final answer.
3. Run a Python-based agent that invokes local functions.
4. Use CSV/JSON data as a source of truth for an agent.
5. Apply a human-approval gate before modifying data.
6. Explain a simple writer–reviewer multi-agent workflow.



---

## 1. What is an AI agent?

A regular chatbot mainly produces text from the conversation. A **tool-using AI agent** can decide which available tool to call, supply arguments, receive the tool's result, and decide what to do next. The AI model *requests* a tool call; the Python application *executes* the function.

```text
User request
     |
     v
 AI agent (chooses next action)
     |
     v
 Tool call ---> Python function / CSV / JSON
     ^                    |
     |---- tool result ---|
     |
     v
Final answer (or another tool call)
```

**Vocabulary:**

- **Agent:** AI model plus instructions, accessible tools, and execution loop.
- **Tool:** A function the application allows the agent to request.
- **Tool call:** The model's structured request to execute a named function.
- **Observation/tool result:** What the Python function returns.
- **Human-in-the-loop:** A person approves or rejects an action before it is performed.
- **Multi-agent workflow:** Two or more agent roles that cooperate on a task.

## 2. One-time environment setup

### Step 1 — Get the code

Download and extract the lab ZIP supplied by your trainer. Open the extracted folder in **VS Code** using **File → Open Folder**.

Your project should include files similar to:

```text
agentic_ai_5_labs/
├── agent_core.py
├── demo_01_calculator.py
├── demo_02_inventory.py
├── demo_03_ticket_agent.py
├── demo_04_report_agent.py
├── demo_05_multi_agent.py
├── requirements.txt
├── .env.example
├── data/
│   ├── inventory.csv
│   ├── tickets.json
│   └── sales.csv
└── output/
```

### Step 2 — Open a terminal

In VS Code, select **Terminal → New Terminal**. Confirm the terminal is in the extracted project folder.

### Step 3 — Create and activate a Python virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> On Windows Command Prompt (`cmd`), use `.venv\Scripts\activate.bat` instead of the PowerShell command.

### Step 4 — Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5 — Configure the Groq API key

Create a file named **`.env`** in the project root (you can copy `.env.example`). Add:

```dotenv
GROQ_API_KEY=replace_with_your_actual_key
GROQ_MODEL=openai/gpt-oss-20b
```

Your trainer may specify another supported tool-capable model. An internet connection and a working Groq API key are required. API access and rate limits depend on your account.

**Security:** Do not share your API key, paste it into screenshots, or commit `.env` to Git. The code package has a `.gitignore` entry for `.env`.

### Step 6 — Verify the setup

```bash
python demo_01_calculator.py
```

The application should prompt for a calculation. If it does not start, see **Troubleshooting** below.

---

## Lab 1 — Calculator Agent: Calling a Python Tool

**Goal:** See how the agent selects a local arithmetic function and returns a grounded answer.

**Scenario:** An employee wants the GST amount and final price for an item.

### Instructions

1. Open `demo_01_calculator.py` in VS Code.
2. Locate the `calculate` function. Observe its `add`, `subtract`, `multiply`, and `divide` operations.
3. Locate the tool schema named `calculate`: this tells the model which arguments it may request.
4. Run:

   ```bash
   python demo_01_calculator.py
   ```

5. Enter this prompt:

   ```text
   What is 18% GST on 1250 rupees? Give the tax and total amount.
   ```

6. Check the terminal for lines beginning with `[Tool call ...]` and `[Tool result]`. Your tool call sequence may vary.
7. Verify the expected values: **GST = ₹225** and **final price = ₹1,475**.
8. Run again and ask: `What is 250 divided by 0?` Observe how the error is reported.

### Participant questions

- Which component decided to use the calculator?
- Did the AI model calculate directly, or did the Python function execute the arithmetic?
- What happens when the function raises an error?

**Success criterion:** You can identify a tool name, its arguments, the tool's response, and the final answer.

---

## Lab 2 — Inventory Agent: Retrieving Data

**Goal:** Let the agent choose a data-retrieval function and use real CSV values.

**Scenario:** A store manager needs to identify products below their reorder threshold.

### Instructions

1. Open `data/inventory.csv` and inspect the columns `sku`, `product`, `quantity`, and `reorder_level`.
2. Open `demo_02_inventory.py` and find the tool functions `list_inventory`, `low_stock_items`, and `lookup_product`.
3. Run:

   ```bash
   python demo_02_inventory.py
   ```

4. Enter:

   ```text
   Check the inventory and tell me which products need to be reordered.
   ```

5. Verify the following source data:

   | Product | Available | Reorder level | Expected status |
   |---|---:|---:|---|
   | Laptop | 5 | 8 | Reorder |
   | Mouse | 40 | 20 | Sufficient |
   | Keyboard | 7 | 10 | Reorder |
   | Monitor | 12 | 6 | Sufficient |
   | USB Cable | 3 | 15 | Reorder |

6. Run the program again and ask: `What is the quantity of SKU P002?` Expected answer: **40**.
7. Note which tool the agent chose for each request.

### Participant questions

- How does the agent access the inventory data?
- Why should the agent not invent missing quantities?
- When is a single-product lookup better than loading all products?

**Success criterion:** You correctly identify all three low-stock products and the function used to retrieve them.

---

## Lab 3 — Helpdesk Agent: Human Approval

**Goal:** Distinguish read-only tool use from actions that modify data.

**Scenario:** An IT support ticket needs its priority increased, but a human must authorize the change.

### Instructions

1. Open `data/tickets.json`. Find ticket `T101` (initially **open** with **medium** priority).
2. Open `demo_03_ticket_agent.py` and look for `get_ticket` and `update_ticket_priority`.
3. Run:

   ```bash
   python demo_03_ticket_agent.py
   ```

4. Enter:

   ```text
   Inspect ticket T101. If it is open, change its priority to high.
   ```

5. If the script asks whether to apply the change, type `NO` first. Reopen `data/tickets.json` and verify that the priority is **still medium**.
6. Run the same request again. This time, if the proposed change is correct, type **`YES`** exactly.
7. Open `data/tickets.json` and verify that `T101` now has **high** priority.
8. To repeat the exercise, manually change the JSON priority for `T101` back to `medium`.

### Participant questions

- Which function reads the ticket, and which function modifies it?
- What prevents an unapproved change?
- What would be the risk if a production agent could update any ticket without authorization?

**Success criterion:** A rejected request leaves the file unchanged; an approved request updates only the intended ticket.

> **Important:** The example writes only to a local training JSON file. Production helpdesk systems need authentication, role-specific permissions, validation, and audit logging.

---

## Lab 4 — Sales Report Agent: Multi-step Execution

**Goal:** Observe an agent perform analysis and persist an output artifact.

**Scenario:** A sales manager requests a brief revenue report from a CSV dataset.

### Instructions

1. Open `data/sales.csv` and review the `month`, `region`, `product`, `units`, and `revenue` fields.
2. Open `demo_04_report_agent.py` and locate the `summarize_sales` and `save_report` tools.
3. Run:

   ```bash
   python demo_04_report_agent.py
   ```

4. Observe the logged calls to read/summarize data and save the report. Tool-selection behavior may vary.
5. Open the generated file: `output/sales_report.md`.
6. Verify these reference totals:

   | Month | Revenue |
   |---|---:|
   | January | ₹267,500 |
   | February | ₹225,000 |
   | March | ₹372,500 |
   | **Overall** | **₹865,000** |

7. Identify the best-performing month: **March**.
8. Check that the report contains calculated values rather than invented numbers.

### Participant questions

- Why should calculations come from Python rather than model guesses?
- Which tool creates the file?
- What should happen if report generation fails or reaches the tool-call limit?

**Success criterion:** The Markdown report is created and its numeric claims match the CSV values.

---

## Lab 5 — Multi-Agent Writer and Reviewer

**Goal:** Understand how separate AI roles cooperate and improve a draft.

**Scenario:** A training organization wants a short lesson and quality review.

### Instructions

1. Open `demo_05_multi_agent.py`.
2. Identify two roles: the **Writer Agent** and the **Reviewer Agent**.
3. Run:

   ```bash
   python demo_05_multi_agent.py
   ```

4. When asked for a topic, enter:

   ```text
   Explain password safety to first-year students.
   ```

5. Read the first draft produced by the writer.
6. Read the reviewer's comments about clarity, accuracy, and completeness.
7. Read the final revised draft.
8. Modify the reviewer instructions to require **simpler language and a practical example**, then run the lab again.
9. Compare both final versions. Note at least two improvements or shortcomings.

### Workflow

```text
User topic
   |
   v
Writer Agent: initial draft
   |
   v
Reviewer Agent: feedback
   |
   v
Writer Agent: one revision
   |
   v
Final lesson
```

### Participant questions

- How are the writer and reviewer responsibilities different?
- Does having two agents guarantee factual correctness?
- What is the benefit of limiting the revision loop?

**Success criterion:** You can explain how feedback from one role influences the output of another role.

> This is a **sequential role-based multi-agent demonstration**. It is not a network of independently running autonomous agents. Review the content for factual accuracy before reuse.

---

## 3. Reflection and completion checklist

Check each item before leaving the lab:

- [ ] I can distinguish a chatbot from a tool-using AI agent.
- [ ] I can identify a tool call and its returned result in terminal output.
- [ ] I can explain how an agent retrieves CSV or JSON data.
- [ ] I can show why human approval is needed before modifying data.
- [ ] I can find and inspect a report generated by the agent.
- [ ] I can describe the writer–reviewer workflow.

### Optional challenge

Choose **one** of the labs and extend it:

- Calculator: add a `percentage` operation.
- Inventory: display how many additional units are needed to reach the reorder level.
- Helpdesk: add a rule that blocks priority changes for closed tickets.
- Sales: include revenue totals grouped by region.
- Writer/Reviewer: introduce a second reviewer for technical accuracy.

Test your change and show the trainer the code, one tool log or workflow trace, and the final result.

## 4. Troubleshooting

| Problem | What to check |
|---|---|
| `python` or `py` is not recognized | Install Python and restart the terminal. Check `python --version` or `py --version`. |
| `ModuleNotFoundError: groq` | Activate the correct `.venv` and run `python -m pip install -r requirements.txt`. |
| API authentication failure | Verify `.env` exists in the project root and contains a valid `GROQ_API_KEY`. |
| Model not available / tool calls rejected | Ask the trainer for an available Groq model that supports tool calling; update `GROQ_MODEL`. |
| Rate limit error | Reduce repeated calls and follow your account's rate-limit guidance. |
| A tool call did not appear | Check the model response and prompt; the model may answer without a tool. Re-run with a task requiring the relevant tool. |
| File not found | Run the script from the extracted project folder and verify all `data/` files are present. |
| PowerShell blocks activation | Use Command Prompt and `.venv\Scripts\activate.bat`, or follow your organization's approved PowerShell policy. |
| Ticket no longer has original priority | Reset ticket `T101` in `data/tickets.json` to `medium`. |

## 5. Further exploration

Once the core execution loop is clear, explore structured agent orchestration, workflow states, conditional branches, and retries using frameworks such as **LangChain** or **LangGraph**.

**End of participant lab guide.**
