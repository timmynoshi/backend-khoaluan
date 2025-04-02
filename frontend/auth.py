# frontend/auth.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import SessionLocal

def login_user(tai_khoan: str, mat_khau: str) -> dict:
    session: Session = SessionLocal()
    try:
        query = text("""
            SELECT Id_NguoiDung, QuyenHan FROM TaiKhoan
            WHERE TaiKhoan = :tk AND MatKhau = :mk
        """)
        result = session.execute(query, {"tk": tai_khoan, "mk": mat_khau}).fetchone()

        if result:
            return {
                "status": "success",
                "id": result[0],
                "quyenHan": result[1]
            }
        else:
            return {"status": "error", "message": "Tài khoản hoặc mật khẩu không đúng"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        session.close()
