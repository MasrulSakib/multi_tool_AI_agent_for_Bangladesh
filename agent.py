"""
agent.py

This file builds the "brain" of our AI agent, exactly as the assignment
asks for: ONE Main Agent, built with LangChain's AgentExecutor, that
owns all four tools:

    - institutions_db_tool
    - hospitals_db_tool
    - restaurants_db_tool
    - web_search_tool

How it works when you ask a question:
    1. The AgentExecutor sends your question, the system instructions,
       and the list of tools to the LLM.
    2. The LLM decides which ONE tool (if any) is needed and calls it -
       this is the "routing" step. A data/statistics question calls the
       matching DB tool; a general knowledge question calls
       web_search_tool.
    3. LangChain runs that tool, feeds the result back to the LLM, and
       the LLM writes the final natural-language answer.

Note: AgentExecutor moved out of `langchain.agents` in LangChain 1.x
(the legacy agent APIs now live in the separate `langchain-classic`
package) - that's why the import below points there instead.
"""

import os

from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

from tools import ALL_TOOLS

# Reads GROQ_API_KEY, MODEL_NAME, and TAVILY_API_KEY from the .env file
# and loads them into the environment.
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError("Please set GROQ_API_KEY in your .env file.")

llm = ChatGroq(model=MODEL_NAME, api_key=GROQ_API_KEY, temperature=0)

# The system prompt tells the LLM exactly how to route each question,
# matching the assignment's routing rules.
SYSTEM_PROMPT = """
You are a helpful assistant for questions about Bangladesh.

Routing rules:
1. If the question asks for specific data, counts, or statistics about
   universities, colleges, madrasahs, or government institutions, use
   institutions_db_tool.
2. If the question is about hospitals, clinics, or health facilities,
   use hospitals_db_tool.
3. If the question is about restaurants, cuisine, ratings, or
   locations, use restaurants_db_tool.
4. Otherwise (general knowledge - definitions, government policy,
   history, culture), use web_search_tool.

When using a DB tool, write a single valid SQLite SELECT query as the
tool input. Never show raw SQL or raw tool output as your final answer
- always explain the result in clear natural language.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# create_tool_calling_agent wires the LLM, tools, and prompt together.
agent = create_tool_calling_agent(llm=llm, tools=ALL_TOOLS, prompt=prompt)

# AgentExecutor is the piece the assignment explicitly asks for: it runs
# the agent's tool-calling loop (call a tool -> feed result back to the
# LLM -> repeat until there's a final answer) and returns the result.
agent_executor = AgentExecutor(agent=agent, tools=ALL_TOOLS, verbose=True)
