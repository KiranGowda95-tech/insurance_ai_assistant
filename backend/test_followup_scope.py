
from langchain_core.messages import HumanMessage, AIMessage
from agent.tool_graph import validate_scope


def test_insurance_follow_up():
    state = {
        "messages": [
            HumanMessage(content="What is the status of claim CLM300001?"),
            AIMessage(content="The claim is Under Review."),
            HumanMessage(content="Which document is missing?"),
            AIMessage(content="The Claim Form is missing."),
            HumanMessage(content="How can I resolve this issue?"),
        ]
    }

    result = validate_scope(state)

    print("Follow-up scope:", result["scope_status"])
    assert result["scope_status"] == "in_scope"


def test_unrelated_question():
    state = {
        "messages": [
            HumanMessage(content="What is the status of claim CLM300001?"),
            AIMessage(content="The claim is Under Review."),
            HumanMessage(content="What is the capital of France?"),
        ]
    }

    result = validate_scope(state)

    print("Unrelated scope:", result["scope_status"])
    assert result["scope_status"] == "out_of_scope"


if __name__ == "__main__":
    test_insurance_follow_up()
    test_unrelated_question()
    print("All follow-up scope tests passed.")
