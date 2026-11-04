SCORES = {"Critical": 10, "Major": 5, "Minor": 2}

def compute_score(findings):
    score = 100
    for f in findings:
        score -= SCORES[f["severity"]]
    return max(score, 0)

if __name__ == "__main__":
    findings = [
        {"issue": "Fire Safety Certificate expired on 15 Aug 2026 (SOP 1.2)", "severity": "Critical"},
        {"issue": "Salary paid on the 9th, deadline is the 7th (SOP 2.2)", "severity": "Major"},
        {"issue": "PF paid on the 18th, deadline is the 15th (SOP 2.1)", "severity": "Minor"},
        {"issue": "1 of 12 vehicles has expired insurance (SOP 3.1)", "severity": "Major"},
        {"issue": "2 of 20 drivers have no background check (SOP 3.2)", "severity": "Major"},
    ]
    print(compute_score(findings))