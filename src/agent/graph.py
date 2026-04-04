from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent import nodes


workflow = StateGraph(AgentState)
workflow.add_node("retrieve" ,nodes.retrieve)
workflow.add_node("generate_node", nodes.generate_node)
workflow.add_node("risk_flagger_node", nodes.risk_flagger_node)

workflow.add_edge(START, "retrieve", )
workflow.add_edge("retrieve","generate_node")
workflow.add_edge("generate_node","risk_flagger_node" )
workflow.add_edge("risk_flagger_node",END)

app = workflow.compile()

initial_state ={
    "question": "What is the Apple risk factor",
    "top_k": 4,
    "source_filter": None,
    "date_from": None
    
}

result =app.invoke(input= initial_state)

print(result)