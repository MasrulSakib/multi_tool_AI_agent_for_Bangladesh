from agent import agent_executor


def main():
    print("Multi-Tool AI Agent for Bangladesh")
    print("Ask about hospitals, institutions, restaurants, or general topics.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        result = agent_executor.invoke({"input": user_input})

        print(f"\nAgent: {result['output']}\n")


if __name__ == "__main__":
    main()
