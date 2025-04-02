from database import SessionLocal
from sqlalchemy.sql import text

def register_tai_khoan(data: dict) -> dict:
    session = SessionLocal()
    try:
        # 1. Thêm vào bảng UngVien
        query_uv = text("""
            INSERT INTO UngVien (Id_UngVien, Ten_UngVien, GioiTinh_UngVien, SDT_UngVien, Email_UngVien, DiaChi_UngVien)
            VALUES (:id, :ten, :gioi_tinh, :sdt, :email, :dia_chi)
        """)
        session.execute(query_uv, {
            "id": data["id"],
            "ten": data["ten"],
            "gioi_tinh": data["gioiTinh"],
            "sdt": data["sdt"],
            "email": data["email"],
            "dia_chi": data["diaChi"]
        })

        # 2. Thêm vào bảng TaiKhoan
        query_tk = text("""
            INSERT INTO TaiKhoan (id, TaiKhoan, MatKhau, QuyenHan, Id_NguoiDung)
            VALUES (:id, :tk, :mk, 'user', :id)
        """)
        session.execute(query_tk, {
            "id": data["id"],
            "tk": data["taiKhoan"],
            "mk": data["matKhau"]
        })

        session.commit()
        return { "status": "success" }

    except Exception as e:
        session.rollback()
        return { "status": "error", "message": str(e) }
    finally:
        session.close()
