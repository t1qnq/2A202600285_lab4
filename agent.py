import os
import sys
import io
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from tools import search_flights, search_hotels, calculate_budget

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    model="qwen/qwen-2.5-72b-instruct",
    temperature=0.7
)
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

def chat(message: str, chat_history: list = None) -> str:
    """
    Hàm chat với agent, hỗ trợ duy trì lịch sử hội thoại.

    Args:
        message: Tin nhắn của người dùng
        chat_history: Lịch sử hội thoại (list của dict {'role': ..., 'content': ...})

    Returns:
        Phản hồi của agent
    """
    # Xây dựng messages list từ history + message mới
    messages = []
    if chat_history:
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=message))

    # Invoke graph
    result = graph.invoke({"messages": messages})
    final = result["messages"][-1]

    return final.content if isinstance(final, AIMessage) else "Xin lỗi, tôi không thể xử lý yêu cầu này."

def main():
    """Vòng lặp chat tương tác trên terminal."""
    print("=" * 60)
    print("🌴 TravelBuddy - Trợ lý du lịch Việt Nam 🌴")
    print("=" * 60)
    print("Gõ 'thoát' hoặc 'quit' để kết thúc.")
    print("Gõ 'reset' để xóa lịch sử hội thoại.\n")

    chat_history = []

    while True:
        try:
            user_input = input("👤 Bạn: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["thoát", "quit", "exit"]:
                print("👋 Tạm biệt! Chúc bạn có chuyến đi vui vẻ!")
                break

            if user_input.lower() == "reset":
                chat_history = []
                print("🔄 Đã xóa lịch sử hội thoại.\n")
                continue

            print("\n🤖 TravelBuddy: ", end="", flush=True)
            response = chat(user_input, chat_history)
            print(response + "\n")

            # Lưu lịch sử hội thoại
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response})

        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt! Chúc bạn có chuyến đi vui vẻ!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}\n")
            print("Vui lòng thử lại.\n")

if __name__ == "__main__":
    main()
