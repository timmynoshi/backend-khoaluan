from database import SessionLocal
from sqlalchemy.sql import text

def get_danh_sach_cong_ty() -> list:
    session = SessionLocal()
    try:
        query = text("""
            SELECT Id_CongTy, Ten_CongTy, SDT_CongTy, DiaChi_CongTy, Email_CongTy, MaSoThue_CongTy
            FROM CongTy
        """)
        results = session.execute(query).fetchall()
        return [
            {
                "id": row[0],
                "ten": row[1],
                "sdt": row[2],
                "diaChi": row[3],
                "email": row[4],
                "maSoThue": row[5]
            }
            for row in results
        ]
    finally:
        session.close()


def add_cong_ty(data: dict) -> dict:
    session = SessionLocal()
    try:
        query = text("""
            INSERT INTO CongTy (Id_CongTy, Ten_CongTy, SDT_CongTy, DiaChi_CongTy, Email_CongTy, MaSoThue_CongTy)
            VALUES (:id, :ten, :sdt, :dia_chi, :email, :mst)
        """)
        session.execute(query, {
            "id": data["id"],
            "ten": data["ten"],
            "sdt": data["sdt"],
            "dia_chi": data["diaChi"],
            "email": data["email"],
            "mst": data["maSoThue"]
        })
        session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

def update_cong_ty(id: str, data: dict) -> dict:
    session = SessionLocal()
    try:
        query = text("""
            UPDATE CongTy
            SET Ten_CongTy = :ten,
                SDT_CongTy = :sdt,
                DiaChi_CongTy = :dia_chi,
                Email_CongTy = :email,
                MaSoThue_CongTy = :mst
            WHERE Id_CongTy = :id
        """)
        session.execute(query, {
            "id": id,
            "ten": data["ten"],
            "sdt": data["sdt"],
            "dia_chi": data["diaChi"],
            "email": data["email"],
            "mst": data["maSoThue"]
        })
        session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        session.close()


def delete_cong_ty(id: str) -> dict:
    session = SessionLocal()
    try:
        # Kiểm tra xem có NTD nào đang dùng công ty này không
        check = session.execute(text("""
            SELECT 1 FROM NhaTuyenDung WHERE Id_Congty = :id
        """), {"id": id}).fetchone()

        if check:
            return {"status": "error", "message": "Không thể xoá. Công ty còn liên kết với nhà tuyển dụng."}

        # Nếu không liên kết thì xoá
        session.execute(text("DELETE FROM CongTy WHERE Id_CongTy = :id"), {"id": id})
        session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        session.close()
