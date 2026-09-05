# Multi-Tool AI Agent for Bangladesh

A command-line AI assistant for Bangladesh-focused questions, built with
**LangChain's `AgentExecutor`**. It routes each question to the right
tool: three SQLite-backed tools for structured data, and a Tavily web
search tool for general knowledge.

## Features

- **Main Agent** (`AgentExecutor`) decides which tool to call for each question.
- **InstitutionsDBTool** answers questions about universities, colleges, madrasahs, and government institutions.
- **HospitalsDBTool** answers questions about hospitals, clinics, and health facilities.
- **RestaurantsDBTool** answers questions about restaurants, cuisine, ratings, and locations.
- **WebSearchTool** (Tavily) handles general questions about Bangladesh - policy, history, culture.

## Project structure

```text
.
├── data/
│   ├── prepare_data.py        # Downloads datasets and builds SQLite databases
│   ├── institutions.db
│   ├── hospitals.db
│   └── restaurants.db
├── tools/
│   ├── db_utils.py            # Shared SQLite helper
│   ├── institutions_tool.py
│   ├── hospitals_tool.py
│   ├── restaurants_tool.py
│   └── web_search_tool.py     # Tavily search integration
├── agent.py                   # LangChain AgentExecutor + tool routing
├── main.py                    # Command-line chat application
├── requirements.txt
└── .env.example
```

## Requirements

- Python 3.10 or later
- A free Groq API key (LLM provider)
- A Tavily API key (web search)

## Setup

1. Clone the repository and enter the project directory.

   ```bash
   git clone <your-repository-url>
   cd bd-multi-tool-agent
   ```

2. Create and activate a virtual environment (recommended).

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Create your environment file and add API keys.

   ```bash
   cp .env.example .env
   ```

   Set `GROQ_API_KEY`, `MODEL_NAME`, and `TAVILY_API_KEY` in `.env`.

5. Build the local databases.

   ```bash
   python data/prepare_data.py
   ```

   This downloads the source datasets from Hugging Face and creates the
   SQLite database files in `data/`. (The repo already ships with these
   three `.db` files pre-built from the real datasets, so this step is
   only needed if you delete them or want to refresh the data.)

6. Start the agent.

   ```bash
   python main.py
   ```

   Type `exit` or `quit` to close the chat.

## How the routing works

`agent.py` builds one `AgentExecutor` with all four tools attached. On
each turn, the LLM reads the system prompt's routing rules and the
user's question, then decides which single tool to call:

| Query                                                     | Routed to          |
| --------------------------------------------------------- | ------------------ |
| `How many hospitals are in Dhaka?`                        | HospitalsDBTool    |
| `Which universities in Bangladesh offer medical degrees?` | InstitutionsDBTool |
| `Find restaurants in Chattogram serving biryani.`         | RestaurantsDBTool  |
| `What is the role of DGHS in Bangladesh?`                 | WebSearchTool      |
| `How many government institutions are in Rajshahi?`       | InstitutionsDBTool |

Each DB tool writes and runs a SQL query against its own database, gets
the raw rows back from `db_utils.run_query()`, and the LLM turns that
into a natural-language answer rather than showing raw SQL or rows.

## A note on the data

The two structured datasets don't cover every field the example queries
imply, since they reflect what the real Hugging Face sources contain:

- **Hospitals dataset** has no bed-count or doctor-count columns, so a
  question like "hospitals with bed capacity" can't be answered from
  this data - the agent will correctly say no matching data was found.
- **Institutions dataset** has no explicit "University" category; it's
  EIIN-level records (schools, colleges, madrasahs, technical
  institutes). Medical-degree-granting institutions show up as "Medical
  College" in the _hospitals_ dataset's `type` column instead.

## Why `langchain-classic`

LangChain 1.x moved the legacy `AgentExecutor` / `create_tool_calling_agent`
APIs out of the main `langchain` package and into the separate
`langchain-classic` package (the new default agent API is
`langchain.agents.create_agent`). Since the assignment specifically
asks for `AgentExecutor`, this project imports it from
`langchain_classic.agents`.

## Data sources

- [Institutional Information of Bangladesh](https://huggingface.co/datasets/Mahadih534/Institutional-Information-of-Bangladesh)
- [All Bangladeshi Hospitals](https://huggingface.co/datasets/Mahadih534/all-bangladeshi-hospitals)
- [Bangladeshi Restaurant Data](https://huggingface.co/datasets/Mahadih534/Bangladeshi-Restaurant-Data)
