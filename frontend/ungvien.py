# frontend/ungvien.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import SessionLocal

def get_thong_tin_ung_vien(id: str) -> dict:
    session: Session = SessionLocal()
    try:
        query = text("""
            SELECT uv.Id_UngVien, uv.Ten_UngVien, uv.GioiTinh_UngVien,
                   uv.SDT_UngVien, uv.Email_UngVien,
                   px.Ten_PhuongXa, qh.Ten_QuanHuyen, tp.Ten_TinhTP
            FROM UngVien uv
            JOIN PhuongXa px ON uv.DiaChi_UngVien = px.Id_PhuongXa
            JOIN QuanHuyen qh ON px.Id_QuanHuyen = qh.Id_QuanHuyen
            JOIN TinhTP tp ON qh.Id_TinhTP = tp.Id_TinhTP
            WHERE uv.Id_UngVien = :id
        """)

        result = session.execute(query, {"id": id}).fetchone()

        if result:
            return {
                "id": result[0],
                "ten": result[1],
                "gioiTinh": result[2],
                "sdt": result[3],
                "email": result[4],
                "diaChi": {
                    "phuong": result[5],
                    "quan": result[6],
                    "tinh": result[7]
                }
            }
        else:
            return {"error": "Không tìm thấy ứng viên"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        session.close()


def update_ung_vien(id: str, data: dict) -> dict:
    session: Session = SessionLocal()
    try:
        query = text("""
            UPDATE UngVien
            SET Ten_UngVien = :ten,
                GioiTinh_UngVien = :gioi_tinh,
                SDT_UngVien = :sdt,
                Email_UngVien = :email,
                DiaChi_UngVien = :dia_chi
            WHERE Id_UngVien = :id
        """)
        session.execute(query, {
            "id": id,
            "ten": data["ten"],
            "gioi_tinh": data["gioiTinh"],
            "sdt": data["sdt"],
            "email": data["email"],
            "dia_chi": data["diaChi"]
        })
        session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        session.close()


def get_danh_sach_ung_vien() -> list:
    session = SessionLocal()
    try:
        query = text("""
            SELECT Id_UngVien, Ten_UngVien, GioiTinh_UngVien, SDT_UngVien, Email_UngVien
            FROM UngVien
        """)
        results = session.execute(query).fetchall()
        return [
            {
                "id": row[0],
                "ten": row[1],
                "gioiTinh": row[2],
                "sdt": row[3],
                "email": row[4]
            }
            for row in results
        ]
    finally:
        session.close()

def add_ung_vien(data: dict) -> dict:
    session = SessionLocal()
    try:
        # Bạn có thể tự sinh Id_UngVien bên client hoặc dùng logic sinh ID ở đây
        query = text("""
            INSERT INTO UngVien (Id_UngVien, Ten_UngVien, GioiTinh_UngVien, SDT_UngVien, DiaChi_UngVien, Email_UngVien)
            VALUES (:id, :ten, :gioi_tinh, :sdt, :dia_chi, :email)
        """)
        session.execute(query, {
            "id": data["id"],
            "ten": data["ten"],
            "gioi_tinh": data["gioiTinh"],
            "sdt": data["sdt"],
            "dia_chi": data["diaChi"],
            "email": data["email"]
        })
        session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

def delete_ung_vien(id: str) -> dict:
    session = SessionLocal()
    try:
        # Kiểm tra ràng buộc khóa ngoại
        check_fk = session.execute(text("""
            SELECT 1 FROM TaiKhoan WHERE Id_NguoiDung = :id
            UNION
            SELECT 1 FROM LichSu WHERE id = :id
            UNION
            SELECT 1 FROM FilterUV WHERE Id_UngVien = :id
        """), {"id": id}).fetchone()

        if check_fk:
            return {"status": "error", "message": "Không thể xoá. Ứng viên còn liên kết dữ liệu."}

        session.execute(text("DELETE FROM UngVien WHERE Id_UngVien = :id"), {"id": id})
        session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        session.close()
