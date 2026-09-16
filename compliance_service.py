import json
import os


RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "rules",
    "rules.json"
)


def load_rules():

    with open(RULES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def check_compliance(information):

    rules = load_rules()

    required_fields = rules["general"]["required_fields"]

    checks = []
    violations = []

    for field in required_fields:

        value = information.get(field)

        if value and str(value).strip():

            checks.append({
                "field": field,
                "status": "PASS",
                "message": "Information detected"
            })

        else:

            checks.append({
                "field": field,
                "status": "FAIL",
                "message": "Information not detected"
            })

            violations.append(field)

    total = len(checks)
    passed = len(
        [check for check in checks if check["status"] == "PASS"]
    )

    score = round((passed / total) * 100, 2) if total else 0

    if score == 100:
        status = "COMPLIANT"

    elif score >= 70:
        status = "NEEDS REVIEW"

    else:
        status = "NON-COMPLIANT"

    return {
        "score": score,
        "status": status,
        "checks": checks,
        "violations": violations
    }