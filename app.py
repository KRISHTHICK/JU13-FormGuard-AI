# app.py – FormGuard AI: Intelligent Form Validator with AI Agent

import streamlit as st
import fitz  # PyMuPDF
import docx2txt
import json
import ollama
import re

# --- Rule Set (can be loaded from external JSON too) ---
def get_validation_rules():
    return {
        "required_fields": ["Employee ID", "Name", "Trip Date", "Total Amount"],
        "format_rules": {
            "Trip Date": r"\\d{4}-\\d{2}-\\d{2}",  # YYYY-MM-DD
            "Total Amount": r"\\$\\d+(\\.\\d{2})?"
        },
        "consistency_checks": [
            {"field1": "Total Amount", "field2": "Sum of Expenses"}
        ]
    }

# --- File Text Extraction ---
def extract_text(file):
    if file.name.endswith(".pdf"):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

# --- Validator Agent using Rules ---
def validate_text_with_rules(text, rules):
    results = {"missing": [], "format_issues": [], "consistency": [], "passed": []}

    for field in rules["required_fields"]:
        if field.lower() not in text.lower():
            results["missing"].append(field)
        else:
            results["passed"].append(field)

    for field, pattern in rules["format_rules"].items():
        match = re.search(pattern, text)
        if not match:
            results["format_issues"].append(f"{field} format incorrect or missing")

    for check in rules["consistency_checks"]:
        val1 = extract_field_value(text, check['field1'])
        val2 = extract_field_value(text, check['field2'])
        if val1 != val2:
            results["consistency"].append(f"Mismatch: {check['field1']} ≠ {check['field2']}")

    return results

# --- Extract value after a field label ---
def extract_field_value(text, field):
    pattern = rf"{field}[:\s]*([\w\$\.\-]+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else ""

# --- Validator Agent Explanation (LLM) ---
def validator_agent_explain(text, validation_result):
    prompt = f"""
You are a smart form validator agent.
Given this document text:
{text[:2000]}

And these validation findings:
{json.dumps(validation_result, indent=2)}

Summarize the issues and provide friendly suggestions to fix them.
"""
    return query_llm(prompt)

# --- Query Ollama LLaMA3 ---
def query_llm(prompt):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# --- Streamlit UI ---
st.set_page_config(page_title="FormGuard AI", layout="wide")
st.title("✅ FormGuard AI – Smart Form Validator with Agent")

uploaded = st.file_uploader("Upload Filled Form (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded:
    with st.spinner("Extracting and validating..."):
        text = extract_text(uploaded)
        rules = get_validation_rules()
        result = validate_text_with_rules(text, rules)
        explanation = validator_agent_explain(text, result)

    st.markdown("### 📋 Validation Report")
    st.json(result)

    st.markdown("### 🤖 Validator Agent Suggestions")
    st.markdown(explanation)
else:
    st.info("Upload a form file to begin validation.")
