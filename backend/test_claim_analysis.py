import json

from services.claim_analysis_service import analyze_claim


def test_existing_claim():
    result = analyze_claim("CLM300001")

    assert result is not None, "Expected the claim to exist."
    assert result["found"] is True
    assert result["claim"]["claim_id"] == "CLM300001"
    assert result["policy"] is not None
    assert isinstance(result["documents"]["missing"], list)
    assert "hospital" in result

    print(json.dumps(result, indent=2, default=str))
    print("\nPASS: SQL claim analysis returned the expected structure.")


def test_unknown_claim():
    result = analyze_claim("CLM_DOES_NOT_EXIST")
    assert result is None
    print("PASS: Unknown claim is handled correctly.")


if __name__ == "__main__":
    test_existing_claim()
    test_unknown_claim()
