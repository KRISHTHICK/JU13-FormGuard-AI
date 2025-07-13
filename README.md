# JU13-FormGuard-AI
GEN AI

 FormGuard AI – Intelligent Document Validator & Compliance Checker
📌 What It Does
FormGuard AI helps users validate the completeness, consistency, and compliance of filled forms or documents using a Validator AI Agent.

It checks for:

🧾 Required fields filled

✅ Value formats (e.g., date, ID, email)

⚖️ Compliance with policies (e.g., SOP, regulatory)

📌 Consistency across sections (e.g., same name or amount repeated)

🧠 What is the Validator Agent?
The Validator Agent is an autonomous AI function that:

Parses structured/unstructured documents

Checks if required elements are present

Validates formats and logic

Gives human-readable validation report (with issues + suggestions)

🔍 Core Features
Feature	Description
📥 Upload filled forms	Supports PDF, DOCX, or scanned text
📋 Define validation rules	JSON config or LLM-powered discovery
🧠 Validator Agent checks	Checks for missing fields, mismatches, format issues
📌 Compliance feedback	Detects if SOP/legal/policy conditions are met
📑 Suggest corrections	AI recommends fixes
📤 Optional export	Generate validation report as PDF or DOCX

🧑‍💻 Tech Stack
Layer	Technology
UI	Streamlit
AI Validator	LLaMA3 via Ollama
Extraction	PyMuPDF / python-docx
Rules Engine	JSON + AI
Export	Python-docx / fpdf (optional)

📁 Sample Use Case
FormGuard AI validates a travel reimbursement form and finds:

json
Copy
Edit
{
  "Issues Found": [
    "Missing employee ID field",
    "Incorrect date format in 'Trip Date': 12-31-2024",
    "Mismatch between total amount and sum of itemized expenses"
  ],
  "Suggested Fixes": [
    "Add 'Employee ID' under Section A",
    "Use date format YYYY-MM-DD",
    "Correct total to match itemized sum"
  ],
  "Compliance Status": "⚠️ Partially Compliant"
}
