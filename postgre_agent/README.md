# LangGraph PostgreSQL Agent

A simple chatbot that allows users to query a PostgreSQL database using natural language. The application uses LangGraph and LangChain to generate SQL queries and execute them against the database through a Gradio interface.

## Features

* Connects to a PostgreSQL database.
* Uses an OpenAI chat model to interpret user questions.
* Executes SQL queries through LangChain's SQL toolkit.
* Restricts execution to `SELECT` statements only.
* Blocks common destructive SQL commands such as `INSERT`, `UPDATE`, and `DELETE`.
* Provides a simple web interface using Gradio.

## Requirements

* Python 3.10+
* PostgreSQL
* OpenAI API key
* Langchain

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URI=postgresql+psycopg2://username:password@host:5432/database
```

## Running

Start the application with:

```bash
python app.py
```

Gradio will launch a local web interface where you can ask questions about your database.

## Example Questions

* Show all tables.
* What columns are in the students table?
* How many rows are in each table?

## Notes

This project wraps LangChain's `sql_db_query` tool with a simple safety check. Only queries that begin with `SELECT` are executed. Queries containing destructive SQL keywords are rejected before being sent to the database.

The safety mechanism is intentionally simple and should not be considered sufficient for production environments.

