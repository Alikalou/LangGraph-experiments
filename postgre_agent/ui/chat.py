import gradio as gr


def build_chat_fn(agent):

    async def chat(message, history):

        messages = []

        for user, assistant in history:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": assistant})

        messages.append({"role": "user", "content": message})

        ###
        # Asynchronous invocation, which allows the program to do other things while waiting for the agent to respond.
        # The response we get is a dictionary, the important key we want from it is "messages",
        # which is a list of messages in the conversation. 
        # We take the last message, since it is what we are looking for and 
        # then access its content "result["messages"][-1].content".
        # These are LangChain details.

        result = await agent.ainvoke({"messages": messages})

        return result["messages"][-1].content

    return chat


def chat_interface(agent):

    return gr.ChatInterface(
        fn=build_chat_fn(agent),

        title="LangGraph PostgreSQL Agent (Clean Version)",

        description=(
            "Ask questions about your PostgreSQL database safely "
            "using LangGraph."
        ),

        examples=[
            "Show all tables",
            "What columns are in the instructor table?",
            "How many rows are in each table?"
        ],

        cache_examples=False
    )