import os
import sys
import io
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# Khởi tạo LLM với cấu hình của OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    model="qwen/qwen-2.5-72b-instruct"
)

print(llm.invoke("Xin chào?").content)