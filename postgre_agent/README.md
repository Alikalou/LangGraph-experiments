# LangGraph PostgreSQL Agent

A chatbot that allows users to query a PostgreSQL database using natural language. The system uses **LangGraph**, **LangChain**, and **OpenAI** to translate user questions into SQL and execute them through a controlled tool layer exposed via a Gradio interface.

## 🚀 Features

* Connects to a PostgreSQL database
* Natural language → SQL generation using OpenAI models
* LangGraph ReAct agent for tool-based reasoning
* Read-only database access using a dedicated PostgreSQL user
* SQL validation using `sqlparse`
* Automatic `LIMIT` enforcement to prevent large result sets
* Gradio-based chat interface

---

## 🛡️ Security Model

This phase follows a **defense-in-depth** approach by enforcing security at both the database and application layers.

### Database Layer

The application connects using a dedicated **read-only PostgreSQL user** with `SELECT` privileges only. The database account cannot modify the database, ensuring that any write operation is rejected regardless of the generated SQL.

### Application Layer

Before execution, every generated query is validated to ensure that:

* Only a single SQL statement is allowed.
* Only `SELECT` queries are executed.
* SQL is parsed using `sqlparse`.
* A `LIMIT` clause (default: 100 rows) is automatically enforced when not provided.

Together, these layers provide application-level query validation and database-enforced read-only access.

---

## 📦 Requirements

* Python 3.10+
* PostgreSQL database
* OpenAI API key

### Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URI=postgresql+psycopg2://readonly_user:password@host:5432/database
```

---

## ▶️ Running the Application

```bash
python app.py
```

After starting, Gradio will launch a local web interface where you can interact with your database.

---

## 💬 Example Questions

* Show all tables
* What columns are in the `students` table?
* How many rows are in each table?
* List the latest records from `orders`
* Count users grouped by country

---

## ⚙️ System Architecture

```text
User
  │
  ▼
Gradio UI
  │
  ▼
LangGraph Agent
  │
  ▼
SQL Validation Layer
(sqlparse + LIMIT enforcement)
  │
  ▼
PostgreSQL
(read-only user)
```
