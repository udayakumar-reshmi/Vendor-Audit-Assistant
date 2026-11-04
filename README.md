# Vendor Compliance Audit Assistant

A GenAI app that audits a vendor submission against a compliance SOP, scores it, and drafts a Corrective Action Plan (CAP) email. Built as a learning project using sample data only.

**Live demo:** <your streamlit link>

## What it does
1. Reads an SOP (rules) and a vendor submission.
2. An LLM finds the real breaches, with the SOP rule for each.
3. Python calculates the compliance score from the SOP's point system.
4. The LLM drafts a CAP email with a deadline calculated in code.

## How it works
- **Chunking:** documents are split at section boundaries, so each chunk is a complete rule.
- **Embeddings and retrieval:** chunks are embedded and stored in Chroma, with metadata filtering so rule questions search only the SOP.
- **Grounded answers (RAG):** the model answers only from retrieved text, cites the rule, and says "I don't know" when the answer isn't there.
- **Audit agent:** the LLM audits and drafts, and code does the score and dates.
- **Interface:** Streamlit.

## Design decisions
- Scoring is done in code, because LLMs are unreliable at arithmetic.
- Temperature is 0, and the severity guide lives in the SOP, so results are repeatable.
- Fixed-size chunking cut facts in half and mixed topics, so I switched to structure-aware chunking.

## Tech
Python, Gemini API, Chroma, Streamlit

## Limitations and next steps
- Uses fake sample data and a small SOP.
- A human should review the CAP email before it is sent.
- Next: PDF upload, a test set to measure accuracy, and retrieving only the relevant SOP sections for large SOPs.

## Run locally
    python3.13 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

Put GEMINI_API_KEY in a .env file.

   ![Audit results](screenshot-results.png)

   ![Draft CAP email](screenshot-email.png)