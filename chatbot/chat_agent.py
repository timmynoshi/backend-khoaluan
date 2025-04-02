# chatbot/chat_agent.py

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage

from chatbot.tools import tools
from chatbot.prompt_template import assistant_prefix
from services.lichsu_service import get_chat_history


# 🔧 Cấu hình LLM (LM Studio hoặc OpenAI local)
llm = ChatOpenAI(
    openai_api_base="http://localhost:1234/v1",  # tuỳ cấu hình của bạn
    openai_api_key="not-needed",
    model_name="local-model",
    temperature=0.7,
)

# 🧠 Bộ nhớ hội thoại
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

# 🤖 Khởi tạo Agent với tools và prompt
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "prefix": assistant_prefix.strip(),
        "handle_parsing_errors": True,  # ⚠️ QUAN TRỌNG: retry khi gặp lỗi parsing
    }
)


# 📜 Hàm load lại lịch sử khi người dùng quay lại
def load_chat_history_for(id_ungvien: str):
    try:
        chat_history: list[BaseMessage] = get_chat_history(id_ungvien)
        if chat_history:  # ✅ Chỉ gán nếu có dữ liệu
            memory.chat_memory.messages = chat_history
        else:
            memory.clear()  # hoặc giữ nguyên bộ nhớ trống
    except Exception as e:
        print("⚠️ Không thể load lịch sử hội thoại:", e)
        memory.clear()
