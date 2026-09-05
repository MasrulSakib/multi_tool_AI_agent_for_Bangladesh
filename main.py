"""
main.py

This is the file you run to start chatting with the agent.

Before running this, make sure you've already run:
    python data/prepare_data.py

Usage:
    python main.py
"""

from agent import agent_executor


def main():
    print("Multi-Tool AI Agent for Bangladesh")
    print("Ask about hospitals, institutions, restaurants, or general topics.")
    print("Type 'exit' to quit.\n")

    # Keep asking for input until the user types "exit" or "quit".
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not user_input:
            # User just pressed Enter with no text - ask again.
            continue

        # agent_executor.invoke() runs the whole loop: the LLM decides
        # which tool (if any) to call, LangChain runs it, and the loop
        # repeats until there's a final answer.
        result = agent_executor.invoke({"input": user_input})

        print(f"\nAgent: {result['output']}\n")


if __name__ == "__main__":
    main()
