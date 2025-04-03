from sqlalchemy.sql import text
from flask import jsonify
from database import SessionLocal  # hoặc cách bạn import Session

def get_lich_su_chat(id_ungvien):
    session = SessionLocal()
    try:
        query = text("""
            SELECT cauhoi, cautraloi, create_at
            FROM LichSu
            WHERE id = :id
            ORDER BY create_at ASC
        """)
        results = session.execute(query, {"id": id_ungvien}).fetchall()
        return jsonify([
            {
                "cauhoi": row[0],
                "cautraloi": row[1],
                "create_at": row[2].isoformat()
            }
            for row in results
        ])
    except Exception as e:
        print("❌ Lỗi khi lấy lịch sử chat:", e)
        return jsonify({"error": "Lỗi server"}), 500
    finally:
        session.close()
