from typing import TypedDict
from langgraph.graph import StateGraph, END

# Define the structure of the shared state using a TypedDict.
# This represents the data that flows through the graph.
class MyState(TypedDict):
    number: int  # The number we will evaluate to determine win or lose

# Define a node that simply prints the received number and returns the state unchanged
def check_number(state: MyState) -> MyState:
    print(f"Received number: {state['number']}")
    return state

# Define the "win" node — logic for when the number meets the win condition
def win(state: MyState) -> MyState:
    print("Win!")
    return state

# Define the "lose" node — logic for when the number fails the win condition
def lose(state: MyState) -> MyState:
    print("Lose!")
    return state

# Define the logic for deciding which path to take based on the number.
# If the number is greater than 5, the flow should go to the "win" node; otherwise, to "lose".
def decide_win_or_lose(state: MyState) -> str:
    return "win" if state["number"] > 5 else "lose"

# Initialize the graph builder with the state schema
builder = StateGraph(MyState)

# Register the nodes in the graph
builder.add_node("check_number", check_number)  # First node that checks the number
builder.add_node("win", win)                    # Node for the "win" path
builder.add_node("lose", lose)                  # Node for the "lose" path

# Set the entry point of the graph — this is where execution starts
builder.set_entry_point("check_number")

# Add conditional branching from the "check_number" node
# The decide_win_or_lose function determines whether to go to "win" or "lose"
builder.add_conditional_edges(
    "check_number",        # Source node
    decide_win_or_lose,    # Function that returns "win" or "lose" based on state
    {
        "win": "win",       # If decision is "win", go to win node
        "lose": "lose",     # If decision is "lose", go to lose node
    }
)

# Define the endpoints of the graph — both win and lose nodes terminate the execution
builder.add_edge("win", END)
builder.add_edge("lose", END)

# Compile the graph into an executable app
app = builder.compile()

# Run the graph with a test input where number > 5 (should print "Win!")
app.invoke({"number": 8})

# Run the graph with a test input where number <= 5 (should print "Lose!")
app.invoke({"number": 2})