# Multi-Tool AI Agent for Bangladesh

A command-line AI assistant for Bangladesh-focused questions. The agent uses Groq for reasoning, SQLite databases for structured local data, and Tavily for current general-information searches.

## Capabilities

- Search and summarize Bangladeshi institution, hospital, and restaurant records.
- Answer local counts, lists, and detail queries with SQLite-backed tools.
- Search the web for general questions about Bangladesh, including policy, history, and culture.
- Route each request automatically to the most suitable tool.

## Architecture

`AgentExecutor` receives the user request and selects one of four tools:

| Tool | Purpose |
| --- | --- |
| `institutions_db_tool` | Educational and government institution data |
| `hospitals_db_tool` | Hospital, clinic, and health-facility data |
| `restaurants_db_tool` | Restaurant names, locations, and ratings |
| `web_search_tool` | General Bangladesh-related web searches via Tavily |

The three database tools query separate SQLite files generated from public Hugging Face datasets. Tool descriptions provide the agent with the table names and query requirements; the assistant turns tool results into a readable response.

## Requirements

- Python 3.10 or later
- A [Groq API key](https://console.groq.com/keys)
- A [Tavily API key](https://app.tavily.com/home)
- Internet access when building the local databases or using web search

## Quick start

1. Clone the repository and enter its directory.

   ```bash
   git clone <repository-url>
   cd Multi_Tool_AI_Agent_for_Bangladesh
   ```

2. Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS or Linux, use `source .venv/bin/activate` instead.

3. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Create a local environment file.

   ```powershell
   Copy-Item .env.example .env
   ```

   On macOS or Linux, use `cp .env.example .env`.

5. Set the following values in `.env`:

   ```env
   GROQ_API_KEY="your-groq-api-key"
   MODEL_NAME="openai/gpt-oss-120b"
   TAVILY_API_KEY="your-tavily-api-key"
   ```

6. Build the local SQLite databases.

   ```bash
   python data/prepare_data.py
   ```

7. Start the assistant.

   ```bash
   python main.py
   ```

   Type `exit` or `quit` to end the session.

## Example questions

- `How many hospitals are in Dhaka?`
- `List government institutions in Rajshahi.`
- `Find restaurants in Chattogram with high ratings.`
- `What is the role of DGHS in Bangladesh?`

## Project structure

```text
.
|-- agent.py                  # Agent configuration and request routing
|-- main.py                   # Command-line application entry point
|-- requirements.txt
|-- .env.example              # Environment-variable template
|-- data/
|   `-- prepare_data.py       # Downloads datasets and creates SQLite files
`-- tools/
    |-- db_utils.py           # Shared SQLite query helper
    |-- institutions_tool.py
    |-- hospitals_tool.py
    |-- restaurants_tool.py
    `-- web_search_tool.py    # Tavily integration
```

## Data sources

- [Institutional Information of Bangladesh](https://huggingface.co/datasets/Mahadih534/Institutional-Information-of-Bangladesh)
- [All Bangladeshi Hospitals](https://huggingface.co/datasets/Mahadih534/all-bangladeshi-hospitals)
- [Bangladeshi Restaurant Data](https://huggingface.co/datasets/Mahadih534/Bangladeshi-Restaurant-Data)

## Notes

- Generated database files and `.env` are excluded from version control. Run `python data/prepare_data.py` after a fresh clone or whenever you want to refresh the source data.
- Never commit API keys. Keep them only in your local `.env` file.
- The agent uses `langchain-classic` because the project relies on the legacy `AgentExecutor` API.
