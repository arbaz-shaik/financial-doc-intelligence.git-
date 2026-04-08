
from typing_extensions import TypedDict, NotRequired

class AgentState(TypedDict):
    question: str
    top_k: int 
    embed_question: list[float]
    context:str
    sources: list[dict]
    answer: str
    route: str
    risk_flags: list[str]
    retrieved_chunks: list[dict] 
    source_filter:NotRequired[str | None]
    date_from:NotRequired[str | None]
    chat_history: list[dict]


