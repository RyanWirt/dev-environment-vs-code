import argparse
import os

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph


def build_agent(model: BaseChatModel):
    def respond(state: MessagesState):
        response = model.invoke(
            [SystemMessage(content="You are a helpful assistant."), *state["messages"]]
        )
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", respond)
    graph.add_edge(START, "agent")
    graph.add_edge("agent", END)
    return graph.compile()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a basic LangGraph chatbot.")
    parser.add_argument("prompt", nargs="?", default="What is LangGraph?")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument(
        "--demo", action="store_true", help="Run offline without an API key."
    )
    args = parser.parse_args()

    if args.demo:
        model = FakeListChatModel(
            responses=["Demo: LangGraph runs agents as graphs of stateful steps."]
        )
    else:
        if not os.getenv("OPENAI_API_KEY"):
            parser.error("Set OPENAI_API_KEY or use --demo to run offline.")
        model = ChatOpenAI(model=args.model)

    result = build_agent(model).invoke(
        {"messages": [HumanMessage(content=args.prompt)]}
    )
    print(result["messages"][-1].content)
