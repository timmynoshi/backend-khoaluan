# chatbot/chat_service.py

from chatbot.chat_agent import agent, load_chat_history_for
from services.lichsu_service import save_to_lichsu, get_ten_ungvien

def handle_chat(id_ungvien: str, message: str) -> str:
    try:
        ten_ungvien = get_ten_ungvien(id_ungvien)
        load_chat_history_for(id_ungvien)

        # Gắn thông tin ứng viên vào nội dung cho LLM hiểu
        full_input = (
            f"Tôi tên là {ten_ungvien}. Mã ID của tôi là {id_ungvien}. "
            f'Tôi muốn hỏi là: "{message}"'
        )

        print(f"👉 [DEBUG] Full input to LLM: {full_input}")

        response = agent.invoke({"input": full_input})

        # Đảm bảo đầu ra có key 'output'
        response_text = (
            response.get("output") if isinstance(response, dict) else str(response)
        )

        # Lưu lại lịch sử hội thoại
        save_to_lichsu(id_ungvien, message, response_text)

        return response_text

    except Exception as e:
        return f"Xin lỗi, có lỗi xảy ra: {str(e)}"
