from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
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

def _count_tokens(messages: Sequence[BaseMessage]) -> int:
    """Rough token estimator for trimming, independent of any provider.

    tiktoken (langchain's default token counter) only knows OpenAI model
    names, so it fails for non-OpenAI models like Inception's mercury-3.
    A ~4-characters-per-token estimate is good enough for trimming.
    """
    total = 0
    for message in messages:
        content = message.content
        text = content if isinstance(content, str) else str(content)
        total += max(1, len(text) // 4)
    return total

model = ChatOpenAI(
    streaming=True,
    model=settings.LLM_MODEL,
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
)

language = translation.get_language()

system_prompt = str(_("localized_gpt_prompt")) + f"You speak {language}"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
])

trimmer = trim_messages(
    max_tokens=5000,
    strategy="last",
    token_counter=_count_tokens,
    include_system=True,
    allow_partial=False,
    start_on="human",
    end_on=("human", "tool"),
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
workflow = StateGraph(state_schema=MessagesState)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
chatbotapp = workflow.compile(checkpointer=memory)
