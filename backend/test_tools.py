from agent.tools import (
    search_policy,
    get_claim_details,
    get_missing_claim_documents,
    get_claim_hospital
)

def run_test(name,tool,arguments):
    print("\n"+"="*60)
    print(name)

    try:
        result=tool.invoke(arguments)
        print(result)

    except Exception as exc:
        print("ERROR:",type(exc).__name__,str(exc))

if __name__=="__main__":
    run_test(
        "POLICY SEARCH",
        search_policy,
        {"query":"What is the amternity waiting period?"}
    )

    run_test(
        "CLAIM DEATILS",
        get_claim_details,
        {"claim_id":"CLM300001"},
    )

    run_test(
        "MISSING DOCUMENTS",
        get_missing_claim_documents,
        {"claim_id":"CLM300001"},
    )

    run_test(
        "HOSPITAL LOOKUP",
        get_claim_hospital,
        {"claim_id":"CLM300001"}
    )
