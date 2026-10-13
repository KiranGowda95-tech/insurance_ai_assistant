from agent.tool_graph import run_tool_agent

TEST_QUERIES=[
    "What is the status of claim CLM300001?",
    "What is the maternity waiting period?",
    "What is the capital of France?",
    "Hello",
    "Can you help me?",
]

if __name__=="__main__":
    for query in TEST_QUERIES:
        print("\n"+"="*60)
        print("QUESTION:",query)

        try:
            result=run_tool_agent(query)

            print("SCOPE:",result["scope_status"])
            print("ANSWER:",result["answer"])
            print("TOOL USED:",result["tools_used"])

        except Exception as exc:
            print("ERROR:",type(exc).__name__,str(exc))