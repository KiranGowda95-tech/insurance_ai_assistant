from agent.tool_graph import run_tool_agent

queries=[
    "What is the maternity waiting period?",
    "What is the status of claim CLM300001?",
    "Which documents are missing for claim CLM300001?",
    "Which hospital is associated with claim CLM300001?",
]

for query in queries:
    print("\n"+"="*60)
    print("QUESTION:",query)

    try:
        result=run_tool_agent(query)

        print("ANSWER:",result["answer"])
        print("TOOLS used:",result["tools_used"])

    except Exception as exc:
        print("ERROR:",type(exc).__name__,str(exc))