# frontend/diachi.py
from sqlalchemy.sql import text
from database import SessionLocal


def get_tinhtp():
    session = SessionLocal()
    try:
        query = text("SELECT Id_TinhTP, Ten_TinhTP FROM TinhTP")
        results = session.execute(query).fetchall()
        return [{"id": row[0], "ten": row[1]} for row in results]
    finally:
        session.close()


def get_quanhuyen(id_tinh):
    session = SessionLocal()
    try:
        query = text("SELECT Id_QuanHuyen, Ten_QuanHuyen FROM QuanHuyen WHERE Id_TinhTP = :id")
        results = session.execute(query, {"id": id_tinh}).fetchall()
        return [{"id": row[0], "ten": row[1]} for row in results]
    finally:
        session.close()


def get_phuongxa(id_quan):
    session = SessionLocal()
    try:
        query = text("SELECT Id_PhuongXa, Ten_PhuongXa FROM PhuongXa WHERE Id_QuanHuyen = :id")
        results = session.execute(query, {"id": id_quan}).fetchall()
        return [{"id": row[0], "ten": row[1]} for row in results]
    finally:
        session.close()


def get_full_diachi(id_px: str) -> dict:
    session = SessionLocal()
    try:
        query = text("""
            SELECT px.Id_PhuongXa, qh.Id_QuanHuyen, tp.Id_TinhTP
            FROM PhuongXa px
            JOIN QuanHuyen qh ON px.Id_QuanHuyen = qh.Id_QuanHuyen
            JOIN TinhTP tp ON qh.Id_TinhTP = tp.Id_TinhTP
            WHERE px.Id_PhuongXa = :id
        """)
        result = session.execute(query, {"id": id_px}).fetchone()
        if result:
            return {
                "idPhuong": result[0],
                "idQuan": result[1],
                "idTinh": result[2]
            }
        return {}
    finally:
        session.close()