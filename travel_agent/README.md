# 🧳 Travel Agent Project

This project contains two simple travel agent programs built with **LangGraph**, **Groq**, **Google Serper**, and **Gradio**.

The goal of the project is to show the difference between:

1. A travel agent **without memory**
2. A travel agent **with memory**

---

## 1. Travel Agent Without Memory

The first program is a basic LangGraph workflow.

It takes one user request, processes it, and returns a travel response.  
It does not remember previous questions or answers.

### What it does

The program follows these steps:

1. Takes the user's travel request
2. Extracts the destination
3. Searches for tourist attractions
4. Searches for current weather
5. Generates a final travel response

### Example

User:

```txt
I want to travel to Paris
```

The agent extracts `Paris`, searches for attractions and weather, then returns a travel plan.

### Main idea

This version is useful for simple one-time questions.

However, if the user asks a follow-up question like:

```txt
What restaurants are good there?
```

The agent may not understand what `there` refers to because it has no memory.

---

## 2. Travel Agent With Memory

The second program is a chatbot-style travel assistant.

It uses LangGraph with `MemorySaver`, so it can remember the conversation during the session.

### What it does

The agent can:

- Answer travel questions
- Search for attractions
- Search for weather
- Search for flights
- Search for restaurants
- Understand follow-up questions using memory

### Example

User:

```txt
I want to travel to Rome
```

Assistant responds with travel information.

User:

```txt
What is the weather there?
```

The assistant understands that `there` means `Rome`.

### Main idea

This version is better for conversations because it keeps track of the previous messages.

---

## Simple Comparison

| Feature | Without Memory | With Memory |
|---|---|---|
| Remembers previous messages | No | Yes |
| Interface | Simple input/output | Chatbot |
| Uses LangGraph | Yes | Yes |
| Uses search tools | Yes | Yes |
| Good for follow-up questions | No | Yes |
| Uses `MemorySaver` | No | Yes |

---

## Technologies Used

- Python
- LangGraph
- LangChain
- Groq Llama 3.1 8B Instant
- Google Serper API
- Gradio
- dotenv

---

## Environment Variables

Create a `.env` file and add:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

---

## Installation

Install the required packages:

```bash
pip install langgraph langchain langchain-community langchain-core langchain-groq gradio python-dotenv requests typing-extensions
```

---


## Project Summary

This project shows how an AI travel assistant can be built in two ways.

The first version is simple and stateless.  
The second version improves the experience by adding memory, tools, and a chat interface.
