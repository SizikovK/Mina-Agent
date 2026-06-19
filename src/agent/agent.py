from typing import Any, Literal
from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from .create_llm import create_llm
from .prompt import SYSTEM_PROMPT
from .tools import TOOLS


class AgentService:
    def __init__(self, max_loops: int = 12):
        self.tools = TOOLS
        self.tools_by_name = {tool.name: tool for tool in self.tools}
        
        self.max_loops = max_loops

        self.model_with_tools = create_llm().bind_tools(self.tools)
        
        self.graph = self._build_graph()

    def _llm_node(self, state: MessagesState):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT.format(context=state["messages"])),
            *state["messages"],
        ]
        response = self.model_with_tools.invoke(messages)
        return {"messages": [response]}

    def _tool_node(self, state: MessagesState):
        result = []
        last_message = state["messages"][-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                tool = self.tools_by_name[tool_call["name"]]
                try:
                    observation = tool.invoke(tool_call["args"])
                except Exception as e:
                    observation = f"Ошибка при выполнении инструмента: {str(e)}"

                result.append(
                    ToolMessage(
                        content=str(observation), 
                        tool_call_id=tool_call["id"]
                    )
                )
        return {"messages": result}

    def _should_continue(self, state: MessagesState) -> Literal["tool_node", "__end__"]:
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tool_node"
        return END

    def _build_graph(self):
        builder = StateGraph(MessagesState)

        builder.add_node("llm_node", self._llm_node)
        builder.add_node("tool_node", self._tool_node)

        builder.add_edge(START, "llm_node")
        builder.add_conditional_edges("llm_node", self._should_continue)
        builder.add_edge("tool_node", "llm_node")

        return builder.compile()

    def generate_response(self, chat_history: list[HumanMessage | AIMessage]) -> str:
        recursion_limit = self.max_loops * 2 + 1
        config = {"recursion_limit": recursion_limit}

        try:
            final_state = self.graph.invoke({"messages": chat_history}, config=config)
        except Exception as e:
            if "recursion_limit" in str(e).lower():
                return "Запрос оказался слишком сложным. Я сделал слишком много шагов и остановился в целях безопасности."
            return f"Ошибка при обработке запроса: {str(e)}"

        last_message = final_state["messages"][-1]
        return str(last_message.content)
