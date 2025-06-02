from django.utils import translation
from django.utils.translation import gettext_lazy as _
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages, MessageGraph
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import trim_messages

# from langgraph.graph import START, MessagesState, StateGraph
from typing_extensions import TypedDict, Annotated
from typing import Sequence
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langgraph.checkpoint.memory import MemorySaver

language = translation.get_language()

# Define State
class State(TypedDict):
    messages: Annotated[Sequence, add_messages]
    language: str

model = ChatOpenAI(streaming=True)

language = translation.get_language()

system_prompt = str(_("localized_gpt_prompt")) + f"You speak {language}"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
])

trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke(
        {"messages": trimmed_messages, "language": language}
    )
    response = model.invoke(prompt)
    return {"messages": response}

# Build LangGraph
# Define a new graph
workflow = StateGraph(state_schema=MessagesState)
# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
