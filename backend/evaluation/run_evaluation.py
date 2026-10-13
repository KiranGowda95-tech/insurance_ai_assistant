
import csv
import json
import re
from pathlib import Path

from services.chat_service import process_chat


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "evaluation_questions.csv"
REPORT_PATH = BASE_DIR / "evaluation" / "evaluation_report.json"


def load_cases():
    """Load evaluation cases, skipping the extra numeric CSV header."""
    cases = []

    with DATASET_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) < 5:
                continue

            if row[0].strip().upper() in {"0", "EVALUATION_ID"}:
                continue

            evaluation_id, policy, question, expected, topic = [
                value.strip() for value in row[:5]
            ]

            if not evaluation_id.startswith("EVAL"):
                continue

            cases.append({
                "id": evaluation_id,
                "policy": policy,
                "question": question,
                "expected": expected,
                "topic": topic,
            })

    return cases


def normalize(text):
    """Normalize case, punctuation, underscores, and whitespace."""
    text = str(text).lower().replace("_", " ")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def has_any(text, phrases):
    """Return True if any normalized phrase appears in the text."""
    return any(normalize(phrase) in text for phrase in phrases)


def validate_answer(case, answer):
    """
    Validate the expected policy-specific facts.

    These checks are tailored to the current five-case evaluation dataset.
    They are not a general-purpose semantic evaluator.
    """
    text = normalize(answer)
    policy = normalize(case["policy"])

    checks = {
        "requested_policy_mentioned": policy in text,
    }

    if case["id"] == "EVAL001":
        checks["maternity_mentioned"] = "maternity" in text
        checks["24_month_waiting_period"] = bool(
            re.search(r"\b24\s+month(?:s)?\b", text)
        )

    elif case["id"] == "EVAL002":
        checks["dental_treatment_mentioned"] = (
            "dental" in text and "treatment" in text
        )
        checks["accident_exception_mentioned"] = "accident" in text
        checks["coverage_exclusion_mentioned"] = has_any(
            text,
            ["not covered", "excluded", "exclusion", "does not cover"],
        )

    elif case["id"] == "EVAL003":
        checks["maternity_mentioned"] = "maternity" in text
        checks["base_plan_mentioned"] = (
            "base critical illness plan" in text
        )
        checks["not_covered_mentioned"] = has_any(
            text,
            ["not covered", "excluded", "not included"],
        )

    elif case["id"] == "EVAL004":
        checks["driving_risk_mentioned"] = has_any(
            text,
            [
                "drunk driving",
                "driving under the influence",
                "driving under influence",
                "intoxication",
                "driving while intoxicated",
            ],
        )
        checks["exclusion_mentioned"] = has_any(
            text,
            ["not covered", "excluded", "exclusion", "not payable"],
        )

    elif case["id"] == "EVAL005":
        checks["preexisting_condition_mentioned"] = (
            "pre existing condition" in text
            or "pre existing conditions" in text
        )
        checks["specific_coverage_exception_mentioned"] = (
            "specifically covered" in text
            or "specifically mentioned as covered" in text
        )
        checks["exclusion_mentioned"] = has_any(
            text,
            ["not covered", "excluded", "exclusion", "generally excluded"],
        )

    else:
        # Unknown cases should not pass silently.
        checks["known_validator_exists"] = False

    return checks


def evaluate_case(case):
    """Run one case through the actual chat service and validate its answer."""
    try:
        result = process_chat(
            f"Regarding {case['policy']}: {case['question']}"
        )

        answer = result.get("answer", "")
        scope_status = result.get("scope_status", "unknown")
        tools_used = result.get("tools_used", [])

        if not isinstance(answer, str) or not answer.strip():
            return {
                **case,
                "passed": False,
                "answer": str(answer),
                "scope_status": scope_status,
                "tools_used": tools_used,
                "checks": {},
                "failed_checks": ["non_empty_answer"],
                "reason": "Empty answer",
            }

        checks = validate_answer(case, answer)
        failed_checks = [
            name for name, passed in checks.items() if not passed
        ]

        passed = scope_status == "in_scope" and not failed_checks

        if scope_status != "in_scope":
            failed_checks.append("scope_status_in_scope")

        return {
            **case,
            "passed": passed,
            "answer": answer,
            "scope_status": scope_status,
            "tools_used": tools_used,
            "checks": checks,
            "failed_checks": failed_checks,
            "reason": (
                "All configured factual checks passed; verify retrieved "
                "policy evidence separately."
                if passed
                else "One or more factual checks or scope validation failed."
            ),
        }

    except Exception as exc:
        return {
            **case,
            "passed": False,
            "answer": "",
            "checks": {},
            "failed_checks": ["execution"],
            "reason": f"Execution error: {type(exc).__name__}: {exc}",
        }


def main():
    cases = load_cases()

    if not cases:
        raise RuntimeError(f"No evaluation cases found in {DATASET_PATH}")

    results = []

    for case in cases:
        result = evaluate_case(case)
        results.append(result)

        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {case['id']} - {case['policy']}")
        print(f"  Question: {case['question']}")
        print(f"  Answer: {result.get('answer', '')[:350]}")
        print(f"  Checks: {result.get('checks', {})}")
        print(f"  Failed checks: {result.get('failed_checks', [])}")
        print(f"  Reason: {result['reason']}")
        print()

    passed_count = sum(result["passed"] for result in results)

    report = {
        "total": len(results),
        "passed": passed_count,
        "failed": len(results) - passed_count,
        "score_percent": round(100 * passed_count / len(results), 2),
        "results": results,
        "evaluation_note": (
            "Passes indicate that configured answer-pattern checks and "
            "scope validation succeeded. They do not independently prove "
            "source grounding, factual completeness, or semantic correctness. "
            "Review answers against the retrieved policy evidence."
        ),
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 50)
    print(
        f"Evaluation: {passed_count}/{len(results)} passed "
        f"({report['score_percent']}%)"
    )
    print(f"Report saved to: {REPORT_PATH}")

    if report["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
