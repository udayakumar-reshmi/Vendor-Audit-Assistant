import os
import sys
import json
import time
from datetime import date, timedelta
from dotenv import load_dotenv
from google import genai
from google.genai import types
from load_docs import load_documents
from score import compute_score, SCORES

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"

def ask_gemini(prompt, as_json=False):
    config = types.GenerateContentConfig(
        temperature=0,
        response_mime_type="application/json" if as_json else None,
    )
    for attempt in range(5):
        try:
            r = client.models.generate_content(model=MODEL, contents=prompt, config=config)
            return r.text
        except Exception:
            time.sleep(8)
    raise RuntimeError("Gemini is busy. Try again in a few minutes.")

def run_audit(sop, vendor):
    audit_prompt = f"""You are a compliance auditor. Today is {date.today()}.
Compare the vendor submission with the SOP. List ONLY real breaches.
Do not list items that are compliant or not applicable.
Return a JSON list. Each item has: "issue" (short, with the SOP rule number),
"severity" (exactly Critical, Major or Minor).
Use the severity stated in the SOP when there is one.

SOP:
{sop}

VENDOR SUBMISSION:
{vendor}"""
    findings = json.loads(ask_gemini(audit_prompt, as_json=True))
    findings = [f for f in findings if f.get("severity") in SCORES]
    score = compute_score(findings)

    deadline = date.today() + timedelta(days=15)
    cap_prompt = f"""Write a short, professional Corrective Action Plan email to the vendor.
List each finding, the action required, and use exactly this deadline: {deadline}.
Findings: {json.dumps(findings)}
Compliance score: {score}/100"""
    email = ask_gemini(cap_prompt)
    return findings, score, email

if __name__ == "__main__":
    vendor_file = sys.argv[1] if len(sys.argv) > 1 else "vendor_a.txt"
    docs = load_documents("data")
    findings, score, email = run_audit(docs["sop.txt"], docs[vendor_file])
    print("FINDINGS")
    for f in findings:
        print("-", f["severity"], ":", f["issue"])
    print("\nCOMPLIANCE SCORE:", score)
    print("\nDRAFT CAP EMAIL")
    print(email)