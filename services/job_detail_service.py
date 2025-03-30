from sqlalchemy import text
from database import SessionLocal



def get_all_job_details():
    session = SessionLocal()
    try:
        query = text("""
            -- tương tự như get_job_details_by_ids nhưng bỏ phần WHERE Id_CongViec IN (...)
            WITH KyNang_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KN.Ten_KyNang, ', ') AS DanhSachKyNang
                FROM CongViec CV
                LEFT JOIN ChiTietKyNang CTK ON CV.Id_CongViec = CTK.Id_CongViec
                LEFT JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                GROUP BY CV.Id_CongViec
            ),
            KyNangMem_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KNM.Ten_KyNangMem, ', ') AS DanhSachKyNangMem
                FROM CongViec CV
                LEFT JOIN ChiTietKyNangMem CTKM ON CV.Id_CongViec = CTKM.Id_CongViec
                LEFT JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                GROUP BY CV.Id_CongViec
            )
            SELECT 
                CV.Id_CongViec, 
                CV.Ten_CongViec, 
                NTD.Ten_NhaTuyenDung,
                CT.Ten_CongTy,
                VT.Ten_ViTri,
                CN.Ten_ChuyenNganh, 
                NGN.Ten_NganhNghe, 
                PX.Ten_PhuongXa, 
                QH.Ten_QuanHuyen, 
                TTP.Ten_TinhTP, 
                CB.Ten_CapBac, 
                TD.Ten_TrinhDo, 
                CM.Ten_ChuyenMon, 
                NN.Ten_NgoaiNgu,
                CV.MucLuong_CongViec,
                CV.DoTuoi_CongViec,
                CV.KinhNghiem_CongViec,
                CV.GioiTinh_CongViec,
                COALESCE(KNCTE.DanhSachKyNang, '') AS DanhSachKyNang,
                COALESCE(KNMCTE.DanhSachKyNangMem, '') AS DanhSachKyNangMem
            FROM CongViec CV 
            INNER JOIN NhaTuyenDung NTD ON CV.Id_NhaTuyenDung = NTD.Id_NhaTuyenDung
            INNER JOIN CongTy CT ON NTD.Id_CongTy = CT.Id_CongTy
            INNER JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri 
            INNER JOIN ChuyenNganh CN ON VT.Id_ChuyenNganh = CN.Id_ChuyenNganh 
            INNER JOIN NganhNghe NGN ON CN.Id_NganhNghe = NGN.Id_NganhNghe
            INNER JOIN PhuongXa PX ON CV.KhuVuc_CongViec = PX.Id_PhuongXa 
            INNER JOIN QuanHuyen QH ON PX.Id_QuanHuyen = QH.Id_QuanHuyen 
            INNER JOIN TinhTP TTP ON QH.Id_TinhTP = TTP.Id_TinhTP
            INNER JOIN CapBac CB ON CV.CapBac_CongViec = CB.Id_CapBac
            INNER JOIN TrinhDo TD ON CV.TrinhDo_CongViec = TD.Id_TrinhDo
            INNER JOIN ChuyenMon CM ON CV.ChuyenMon_CongViec = CM.Id_ChuyenMon
            INNER JOIN NgoaiNgu NN ON CV.NgoaiNgu_CongViec = NN.Id_NgoaiNgu
            LEFT JOIN KyNang_CTE KNCTE ON CV.Id_CongViec = KNCTE.Id_CongViec
            LEFT JOIN KyNangMem_CTE KNMCTE ON CV.Id_CongViec = KNMCTE.Id_CongViec
        """)
        result = session.execute(query)
        return [dict(zip(result.keys(), row)) for row in result.fetchall()]
    except Exception as e:
        print("❌ Lỗi get_all_job_details:", e)
        return []
    finally:
        session.close()




def get_job_details_by_ids(job_ids):
    if not job_ids:
        return []

    session = SessionLocal()
    try:
        # Tạo chuỗi param: id1, id2, ...
        param_keys = [f"id_{i}" for i in range(len(job_ids))]
        placeholders = ", ".join(f":{key}" for key in param_keys)

        # Dữ liệu mapping: {"id_0": "CV01", "id_1": "CV02", ...}
        params = {f"id_{i}": job_id for i, job_id in enumerate(job_ids)}

        query = text(f"""
            WITH KyNang_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KN.Ten_KyNang, ', ') AS DanhSachKyNang
                FROM CongViec CV
                LEFT JOIN ChiTietKyNang CTK ON CV.Id_CongViec = CTK.Id_CongViec
                LEFT JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                GROUP BY CV.Id_CongViec
            ),
            KyNangMem_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    STRING_AGG(KNM.Ten_KyNangMem, ', ') AS DanhSachKyNangMem
                FROM CongViec CV
                LEFT JOIN ChiTietKyNangMem CTKM ON CV.Id_CongViec = CTKM.Id_CongViec
                LEFT JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                GROUP BY CV.Id_CongViec
            )
            SELECT 
                CV.Id_CongViec, 
                CV.Ten_CongViec, 
                NTD.Ten_NhaTuyenDung, 
                CT.Ten_CongTy,
                VT.Ten_ViTri,
                CN.Ten_ChuyenNganh, 
                NGN.Ten_NganhNghe, 
                PX.Ten_PhuongXa, 
                QH.Ten_QuanHuyen, 
                TTP.Ten_TinhTP, 
                CB.Ten_CapBac, 
                TD.Ten_TrinhDo, 
                CM.Ten_ChuyenMon, 
                NN.Ten_NgoaiNgu,
                CV.MucLuong_CongViec,
                CV.DoTuoi_CongViec,
                CV.KinhNghiem_CongViec,
                CV.GioiTinh_CongViec,
                COALESCE(KNCTE.DanhSachKyNang, '') AS DanhSachKyNang,
                COALESCE(KNMCTE.DanhSachKyNangMem, '') AS DanhSachKyNangMem
            FROM CongViec CV 
            INNER JOIN NhaTuyenDung NTD ON CV.Id_NhaTuyenDung = NTD.Id_NhaTuyenDung
            INNER JOIN CongTy CT ON NTD.Id_CongTy = CT.Id_CongTy
            INNER JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri 
            INNER JOIN ChuyenNganh CN ON VT.Id_ChuyenNganh = CN.Id_ChuyenNganh 
            INNER JOIN NganhNghe NGN ON CN.Id_NganhNghe = NGN.Id_NganhNghe
            INNER JOIN PhuongXa PX ON CV.KhuVuc_CongViec = PX.Id_PhuongXa 
            INNER JOIN QuanHuyen QH ON PX.Id_QuanHuyen = QH.Id_QuanHuyen 
            INNER JOIN TinhTP TTP ON QH.Id_TinhTP = TTP.Id_TinhTP
            INNER JOIN CapBac CB ON CV.CapBac_CongViec = CB.Id_CapBac
            INNER JOIN TrinhDo TD ON CV.TrinhDo_CongViec = TD.Id_TrinhDo
            INNER JOIN ChuyenMon CM ON CV.ChuyenMon_CongViec = CM.Id_ChuyenMon
            INNER JOIN NgoaiNgu NN ON CV.NgoaiNgu_CongViec = NN.Id_NgoaiNgu
            LEFT JOIN KyNang_CTE KNCTE ON CV.Id_CongViec = KNCTE.Id_CongViec
            LEFT JOIN KyNangMem_CTE KNMCTE ON CV.Id_CongViec = KNMCTE.Id_CongViec
            WHERE CV.Id_CongViec IN ({placeholders})
        """)

        result = session.execute(query, params)
        jobs = [dict(zip(result.keys(), row)) for row in result.fetchall()]

        # 🧠 Sắp xếp lại theo đúng thứ tự của job_ids đầu vào
        job_map = {job["Id_CongViec"]: job for job in jobs}
        ordered_jobs = [job_map[job_id] for job_id in job_ids if job_id in job_map]

        return ordered_jobs

    except Exception as e:
        return {"error": str(e)}

    finally:
        session.close()
