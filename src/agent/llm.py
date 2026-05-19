from langchain.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from typing import Any, Literal
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
import json

from create_llm import create_llm   
from tools import *

POLICIES = [
    "Идет тестирование функционала инструментов.",
    "Если тебе нужно выполнить какое-то действие, используй инструменты, которые у тебя есть.",
    'В ответ верни только валидный JSON вида {{"status": "success", "content": "Ответ"}} или {{"status": "need_details", "content": "Что нужно уточнить"}}.'
]

SYSTEM_PROMPT = (
    "Ты агент помощник по имени Мина.\n\n"
    "Правила:\n"
    + "\n".join(f"- {policy}" for policy in POLICIES)
)


tools = [multiply, add, divide, parce_cryptocurrencies, parce_weather]
tools_by_name = {tool.name: tool for tool in tools}
agent: Any | None = None

def llm_node(state: MessagesState):
    llm_with_tools = create_llm().bind_tools(tools)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT.format(context=state["messages"])),
        *state["messages"],
    ]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool_node"

    return END

def create_graph():
    agent_builder = StateGraph(MessagesState)

    agent_builder.add_node("llm_node", llm_node)
    agent_builder.add_node("tool_node", tool_node)

    agent_builder.add_edge(START, "llm_node")
    agent_builder.add_conditional_edges(
        "llm_node",
        should_continue,
        ["tool_node", END]
    )
    agent_builder.add_edge("tool_node", "llm_node")

    return agent_builder.compile()

def get_agent():
    global agent
    if agent is None:
        agent = create_graph()
    return agent

agent = get_agent()

messages = [HumanMessage(content="Что сейчас с биткоином? Какая у него капитализация? Какая погода в городе Мурино?")]
messages = agent.invoke({"messages": messages})

last_message = messages["messages"][-1]
content = json.loads(last_message.content)
if content["status"] == "need_details":
    messages = agent.invoke(content["content"])

for m in messages["messages"]:
    m.pretty_print()






