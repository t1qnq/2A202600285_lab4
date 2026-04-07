import os
import sys
import io
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from tools import search_flights, search_hotels, calculate_budget

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# Đọc system prompt từ file
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Khởi tạo LLM với OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    model="qwen/qwen-2.5-72b-instruct",
    temperature=0.7
)

# Danh sách tools
tools = [search_flights, search_hotels, calculate_budget]

# Tạo agent với LangChain v1.2+ API
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)

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
        messages.extend(chat_history)
    messages.append({"role": "user", "content": message})
    
    # Stream qua agent
    last_response = None
    for chunk in agent.stream({"messages": messages}, stream_mode="updates"):
        # chunk là dict với key là node name ('model' hoặc 'tools')
        for node_name, node_data in chunk.items():
            if "messages" in node_data:
                for msg in node_data["messages"]:
                    if isinstance(msg, AIMessage) and not msg.tool_calls:
                        last_response = msg.content
    
    return last_response or "Xin lỗi, tôi không thể xử lý yêu cầu này."

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
