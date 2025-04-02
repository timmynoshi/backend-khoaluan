from sqlalchemy.sql import text
from database import SessionLocal

# Lấy Ngành nghề
def get_nganhnghe():
    session = SessionLocal()
    try:
        query = text("SELECT Id_NganhNghe, Ten_NganhNghe FROM NganhNghe")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Chuyên ngành theo Ngành nghề
def get_chuyennganh(id_nganh):
    session = SessionLocal()
    try:
        query = text("SELECT Id_ChuyenNganh, Ten_ChuyenNganh FROM ChuyenNganh WHERE Id_NganhNghe = :id_nganh")
        result = session.execute(query, {"id_nganh": id_nganh})
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Vị trí chuyên môn theo Chuyên ngành
def get_vitri(id_cn):
    session = SessionLocal()
    try:
        query = text("SELECT Id_ViTri, Ten_ViTri FROM ViTriChuyenMon WHERE Id_ChuyenNganh = :id_cn")
        result = session.execute(query, {"id_cn": id_cn})
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Tỉnh/Thành phố
def get_tinhtpp():
    session = SessionLocal()
    try:
        query = text("SELECT Id_TinhTP, Ten_TinhTP FROM TinhTP")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Quận/Huyện theo Tỉnh
def get_quanhuyenn(id_tinh):
    session = SessionLocal()
    try:
        query = text("SELECT Id_QuanHuyen, Ten_QuanHuyen FROM QuanHuyen WHERE Id_TinhTP = :id_tinh")
        result = session.execute(query, {"id_tinh": id_tinh})
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Phường/Xã theo Quận
def get_phuongxaa(id_quan):
    session = SessionLocal()
    try:
        query = text("SELECT Id_PhuongXa, Ten_PhuongXa FROM PhuongXa WHERE Id_QuanHuyen = :id_quan")
        result = session.execute(query, {"id_quan": id_quan})
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Trình độ
def get_trinhdo():
    session = SessionLocal()
    try:
        query = text("SELECT Id_TrinhDo, Ten_TrinhDo FROM TrinhDo")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Cấp bậc
def get_capbac():
    session = SessionLocal()
    try:
        query = text("SELECT Id_CapBac, Ten_CapBac FROM CapBac")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Kỹ năng
def get_kynang():
    session = SessionLocal()
    try:
        query = text("SELECT Id_KyNang, Ten_KyNang FROM KyNang")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Kỹ năng mềm
def get_kynangmem():
    session = SessionLocal()
    try:
        query = text("SELECT Id_KyNangMem, Ten_KyNangMem FROM KyNangMem")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Chuyên môn
def get_chuyenmon():
    session = SessionLocal()
    try:
        query = text("SELECT Id_ChuyenMon, Ten_ChuyenMon FROM ChuyenMon")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()

# Lấy Ngoại ngữ
def get_ngoaingu():
    session = SessionLocal()
    try:
        query = text("SELECT Id_NgoaiNgu, Ten_NgoaiNgu FROM NgoaiNgu")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        session.close()
