# services/lichsu_service.py
from database import SessionLocal
from sqlalchemy import text


def save_to_lichsu(id_ungvien: str, cauhoi: str, cautraloi: str):
    session = SessionLocal()
    try:
        query = text("""
            INSERT INTO LichSu (id, cauhoi, cautraloi)
            VALUES (:id, :cauhoi, :cautraloi)
        """)
        session.execute(query, {
            "id": id_ungvien,
            "cauhoi": cauhoi,
            "cautraloi": str(cautraloi)
        })
        session.commit()
    except Exception as e:
        print("❌ Lỗi khi ghi lịch sử:", e)
    finally:
        session.close()


def get_ten_ungvien(id_ungvien: str) -> str:
    session = SessionLocal()
    try:
        query = text("SELECT Ten_UngVien FROM UngVien WHERE Id_UngVien = :id")
        result = session.execute(query, {"id": id_ungvien}).fetchone()
        return result[0] if result else "bạn"
    except:
        return "bạn"
    finally:
        session.close()


def get_chat_history(id_ungvien: str) -> list:
    """
    Trả lại lịch sử hội thoại của người dùng dưới dạng list[BaseMessage]
    """
    from langchain_core.messages import AIMessage, HumanMessage

    session = SessionLocal()
    try:
        query = text("""
            SELECT cauhoi, cautraloi FROM LichSu
            WHERE id = :id ORDER BY id DESC
        """)
        rows = session.execute(query, {"id": id_ungvien}).fetchall()

        # Trả về list các message cũ (mỗi dòng là Human -> AI)
        history = []
        for row in rows:
            history.append(HumanMessage(content=row.cauhoi))
            history.append(AIMessage(content=row.cautraloi))
        return history[::-1]  # Đảo ngược để đúng thứ tự hội thoại

    except Exception as e:
        print("❌ Lỗi khi lấy lịch sử hội thoại:", e)
        return []

    finally:
        session.close()
