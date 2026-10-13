
from agent.graph import run_agent

test_queries = [
    "What is the maternity waiting period?",
    "What is the status of claim CLM300001?",
    "Which documents are missing for claim CLM300001?",
    "Which hospital is associated with claim CLM300001?",
]

for query in test_queries:
    print("\n" + "=" * 60)
    print("QUESTION:", query)

    try:
        result = run_agent(query)

        print("INTENT:", result.get("intent", "MISSING"))
        print("ANSWER:", result.get("answer", "MISSING"))
        print("SOURCES:", result.get("sources", []))

    except Exception as exc:
        print("ERROR:", type(exc).__name__, str(exc))
