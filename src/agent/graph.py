from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent import nodes

def route_decision(state : AgentState)->str:
    return state["route"]


workflow = StateGraph(AgentState)
workflow.add_node("router", nodes.router)

workflow.add_conditional_edges("router", route_decision,{
    "sec": "retrieve",
    "news": "retrieve",
    "general": "retrieve"

} )




workflow.add_node("retrieve" ,nodes.retrieve) 
workflow.add_node("generate_node", nodes.generate_node)
workflow.add_node("risk_flagger_node", nodes.risk_flagger_node)

workflow.add_edge(START, "router")
workflow.add_edge("retrieve","generate_node")
workflow.add_edge("generate_node","risk_flagger_node" )
workflow.add_edge("risk_flagger_node",END)

app = workflow.compile()

initial_state ={
    "question": "Tell me about Apple as a company",
    "top_k": 4,
    "source_filter": None,
    "date_from": None
    
}

result =app.invoke(input= initial_state)

print(f" question:   ,{result["question"]}answer: {result["answer"][:100]},  path : {result["route"]}")