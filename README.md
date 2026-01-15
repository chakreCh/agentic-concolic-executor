# Agentic Concolic Execution (ACE) Engine

## 🚀 Project Overview
This project is an **independent implementation** of an Agentic Concolic Execution system. It demonstrates how Large Language Models (LLMs) can be used to replace complex symbolic solvers in software testing.

Instead of using brute-force mathematics to find bugs, this engine uses **AI Reasoning (Google Gemini)** to:
1.  **Read** the execution trace of a program.
2.  **Analyze** logical branches (True/False).
3.  **Propose** targeted inputs to explore new paths.

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **AI Agent:** Google Gemini 1.5 Flash (via `google-genai` SDK)
* **Architecture:** Custom Orchestrator-Agent Pattern
* **Tools:** VS Code, Git

## 📂 Project Structure
* `ace_engine.py`: The main engine containing the Target Program, Tracer, and AI Agent.

## 🧠 How It Works
1.  **Target:** A Python function with hidden bugs and complex branching logic.
2.  **Tracer:** A custom class that records the "path" the code takes during execution.
3.  **Agent:** The LLM analyzes the trace and suggests new `(x, y)` inputs to reach unexplored code.
4.  **Loop:** The system iteratively hunts for bugs until the target is found.

## ⚡ How to Run
1.  Clone the repository.
2.  Install dependencies: `pip install google-genai`
3.  Add your API Key in `ace_engine.py`.
4.  Run: `python ace_engine.py`

---
*Created by Chandan Akhil Reddy Challa*