from typing import TypedDict, Annotated, List
import operator
import os
import requests
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_community.utilities import GoogleSerperAPIWrapper
import gradio as gr


# =========================
# ENV SETUP
# =========================
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


# =========================
# TOOLS
# =========================
serper = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)


def call_groq_llm(messages, model="llama-3.1-8b-instant"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 1500,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("Groq error:", response.text)
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


# =========================
# STATE
# =========================
class TravelState(TypedDict):
    user_input: str
    destination: str
    attractions: str
    weather: str
    final: str
    error: List[str]


# =========================
# NODES
# =========================

def extract_destination(state: TravelState) -> TravelState:
    try:
        messages = [
            {
                "role": "system",
                "content": "Extract only the travel destination from the user message.",
            },
            {"role": "user", "content": state["user_input"]},
        ]

        destination = call_groq_llm(messages).strip()
        return {"destination": destination}

    except Exception as e:
        state["error"].append(f"Destination error: {e}")
    return state
    


def get_attractions(state: TravelState) -> TravelState:
    try:
        query = f"top tourist attractions in {state['destination']}"
        result = serper.run(query)
        return {"attractions": result}
    except Exception as e:
        state["error"].append(f"Attractions error: {e}")

    return state


def get_weather(state: TravelState) -> TravelState:
    try:
        query = f"current weather in {state['destination']}"
        result = serper.run(query)
        return {"weather": result}
    except Exception as e:
        state["error"].append(f"Weather error: {e}")

    return state

def final_response(state):
    attractions = state.get("attractions") or "No data found"
    weather = state.get("weather") or "No weather data available"

    messages = [
        {
            "role": "system",
            "content": "You are a helpful travel assistant.",
        },
        {
            "role": "user",
            "content": f"""
            User asked: {state['user_input']}

            Destination: {state['destination']}

            Attractions:
            {attractions}

            Weather:
            {weather}
            """,
        },
    ]

    result = call_groq_llm(messages, model="llama-3.1-8b-instant")
    return {"final": result}

# =========================
# GRAPH
# =========================
graph_builder = StateGraph(TravelState)

graph_builder.add_node("extract_destination", extract_destination)
graph_builder.add_node("attractions", get_attractions)
graph_builder.add_node("weather", get_weather)
graph_builder.add_node("final", final_response)

graph_builder.add_edge(START, "extract_destination")

# fan-out
graph_builder.add_edge("extract_destination", "attractions")
graph_builder.add_edge("extract_destination", "weather")

# converge
graph_builder.add_edge("attractions", "final")
graph_builder.add_edge("weather", "final")

graph_builder.add_edge("final", END)

graph = graph_builder.compile()


# =========================
# GRADIO WRAPPER
# =========================
def run_agent(user_input):
    state = TravelState(
        user_input=user_input,
        destination="",
        attractions="",
        weather="",
        error=[],
    )

    result = graph.invoke(state)
    print("DEST:", result["destination"])
    print("WEATHER:", result["weather"])
    print("ATTRACTIONS LENGTH:", len(result["attractions"]))

    if result.get("error"):
        return "\n".join(result["error"])

    return result.get("final", "No output")



# =========================
# UI
# =========================


gr.Interface(
    fn=run_agent,
    inputs=gr.Textbox(label="Where do you want to travel?"),
    outputs=gr.Textbox(label="Travel Plan"),
    title="🧳 Travel Agent",
).launch()

