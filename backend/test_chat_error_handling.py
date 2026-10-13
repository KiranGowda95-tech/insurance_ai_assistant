
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


client = TestClient(app, raise_server_exceptions=False)



def test_agent_failure_returns_safe_error():
    """Verify that agent failures return a safe HTTP error."""

    with patch(
        "services.chat_service.run_tool_agent",
        side_effect=RuntimeError("SECRET internal database details"),
    ):
        response = client.post(
            "/api/chat",
            json={"query": "What is the status of claim CLM300001?"},
        )

    print("HTTP STATUS:", response.status_code)
    print("RESPONSE BODY:", response.text)

    assert response.status_code == 500
    assert "SECRET" not in response.text
    assert "internal database details" not in response.text

    print("PASS: Agent failure returns a safe HTTP 500 response.")


def test_agent_recovers_after_failure():
    """Verify a subsequent request succeeds after a simulated failure."""

    mock_result = {
        "query": "What is the status of claim CLM300001?",
        "answer": 'The claim status is "Under Review."',
        "tools_used": ["get_claim_details"],
        "scope_status": "in_scope",
    }

    with patch(
        "services.chat_service.run_tool_agent",
        return_value=mock_result,
    ):
        response = client.post(
            "/api/chat",
            json={"query": "What is the status of claim CLM300001?"},
        )

    assert response.status_code == 200

    body = response.json()
    assert body["answer"] == 'The claim status is "Under Review."'
    assert body["tools_used"] == ["get_claim_details"]
    assert body["scope_status"] == "in_scope"

    print("PASS: The API handles a subsequent successful request.")


if __name__ == "__main__":
    tests = [
        test_agent_failure_returns_safe_error,
        test_agent_recovers_after_failure,
    ]

    for test in tests:
        test()

    print(f"\nAll {len(tests)} error-handling tests passed!")
