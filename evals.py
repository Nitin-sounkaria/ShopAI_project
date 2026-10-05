from shopping_agent import agent


TEST_CASES = [
    {
        "name": "Organic honey with budget",
        "query": "I want organic honey under $20",
        "expected_tool": "search_products",
    },
    {
        "name": "Honey with price limit",
        "query": "Find honey under $15",
        "expected_tool": "search_products",
    },
    {
        "name": "Order history",
        "query": "Show me my previous orders",
        "expected_tool": "order_history",
    },
    {
        "name": "Saved preferences",
        "query": "What are my saved shopping preferences?",
        "expected_tool": "get_preferences",
    },
]


def run_test(test_case):

    print("\n" + "=" * 60)
    print(f"TEST: {test_case['name']}")
    print(f"USER: {test_case['query']}")
    print("=" * 60)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": test_case["query"],
                }
            ]
        }
    )

    messages = result.get("messages", [])

    print("\nTOOL CALLS:")

    found_expected_tool = False

    for message in messages:

        tool_calls = getattr(message, "tool_calls", [])

        for tool_call in tool_calls:

            tool_name = tool_call.get("name")

            print(f"  - {tool_name}")

            if tool_name == test_case["expected_tool"]:
                found_expected_tool = True

    print("\nEXPECTED TOOL:")
    print(f"  {test_case['expected_tool']}")

    print("\nRESULT:")

    if found_expected_tool:
        print("  ✅ PASS")
    else:
        print("  ❌ FAIL")

    return found_expected_tool


if __name__ == "__main__":

    print("\n🧪 AI SHOPPING AGENT EVALUATION")

    passed = 0
    total = len(TEST_CASES)

    for test_case in TEST_CASES:

        if run_test(test_case):
            passed += 1

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed!")

    else:
        print("⚠️ Some tests failed.")