from langgraph.prebuilt import create_react_agent

def build_agent(model, tools):

    return create_react_agent(
        model=model,
        tools=tools
    )