from agent.tool_graph import validate_scope

def check_scope(query:str)->str:
    state={
        "messages":[
            {
                "role":"user","content":query
            }
        ]
    }

    result=validate_scope(state)
    return result["scope_status"]


def test_claim_question():
    assert check_scope(
        "What is the status of claim CLM300001?"
    )=="in_scope"


def test_policy_question():
    assert check_scope(
        "What is the maternity waiting period?"
    )=="in_scope"


def test_unrelated_question():
    assert check_scope(
        "What is the capital of France?"
    )=="out_of_scope"


def test_gresting():
    assert check_scope("Hello")=="clarification"


def test_empty_question():
    assert check_scope("")=="clarification"


    
def test_missing_documents_question():
    print("Entering into this missing document func")
    query = "Which documents are missing for claim CLM300001?"
    actual = check_scope(query)

    print("Missing-documents scope:", actual)

    assert actual == "in_scope"


if __name__=="__main__":
    tests=[
        test_claim_question,
        test_policy_question,
        test_unrelated_question,
        test_gresting,
        test_empty_question,
        test_missing_documents_question
    ]


    for test in tests:
        test()
        print(f"PASS:{test.__name__}")

    print(f"\nAll {len(tests)} tests passed!")


