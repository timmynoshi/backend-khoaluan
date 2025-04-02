from sqlalchemy import text
from database import SessionLocal

def get_jobs_by_filters(id_ungvien, filters):
    session = SessionLocal()


    try:
        query = text("""
            DECLARE @ViTri NVARCHAR(100) = :ViTri;
            DECLARE @ChuyenNganh NVARCHAR(100) = :ChuyenNganh;
            DECLARE @NganhNghe NVARCHAR(100) = :NganhNghe;
            DECLARE @PhuongXa NVARCHAR(100) = :PhuongXa;
            DECLARE @QuanHuyen NVARCHAR(100) = :QuanHuyen;
            DECLARE @TinhTP NVARCHAR(100) = :TinhTP;
            DECLARE @CapBac NVARCHAR(100) = :CapBac;
            DECLARE @TrinhDo NVARCHAR(100) = :TrinhDo;
            DECLARE @ChuyenMon NVARCHAR(100) = :ChuyenMon;
            DECLARE @NgoaiNgu NVARCHAR(100) = :NgoaiNgu;
            DECLARE @KyNang NVARCHAR(MAX) = :KyNang;
            DECLARE @KyNangMem NVARCHAR(MAX) = :KyNangMem;
            DECLARE @MucLuongMin INT = :MucLuongMin;
            DECLARE @MucLuongMax INT = :MucLuongMax;
            DECLARE @DoTuoiMin INT = :DoTuoiMin;
            DECLARE @DoTuoiMax INT = :DoTuoiMax;
            DECLARE @GioiTinh NVARCHAR(10) = :GioiTinh;
            DECLARE @KinhNghiem INT = :KinhNghiem;

            -- CTE 1: Lấy danh sách kỹ năng
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
            ),
            -- CTE 2: Tính số kỹ năng khớp
            MatchScore_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    COUNT(DISTINCT KN.Ten_KyNang) AS MatchKyNang
                FROM CongViec CV
                LEFT JOIN ChiTietKyNang CTK ON CV.Id_CongViec = CTK.Id_CongViec
                LEFT JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                WHERE KN.Ten_KyNang IN (SELECT value FROM STRING_SPLIT(@KyNang, ','))
                GROUP BY CV.Id_CongViec
            ),
            MatchScoreMem_CTE AS (
                SELECT 
                    CV.Id_CongViec,
                    COUNT(DISTINCT KNM.Ten_KyNangMem) AS MatchKyNangMem
                FROM CongViec CV
                LEFT JOIN ChiTietKyNangMem CTKM ON CV.Id_CongViec = CTKM.Id_CongViec
                LEFT JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                WHERE KNM.Ten_KyNangMem IN (SELECT value FROM STRING_SPLIT(@KyNangMem, ','))
                GROUP BY CV.Id_CongViec
            )
            SELECT 
                CV.Id_CongViec, 
                CV.Ten_CongViec, 
                NTD.Ten_NhaTuyenDung, 
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
                COALESCE(KNMCTE.DanhSachKyNangMem, '') AS DanhSachKyNangMem,
                COALESCE(MSC.MatchKyNang, 0) + COALESCE(MSM.MatchKyNangMem, 0) AS MatchScore -- Tổng điểm khớp kỹ năng
            FROM CongViec CV 
            INNER JOIN NhaTuyenDung NTD ON CV.Id_NhaTuyenDung = NTD.Id_NhaTuyenDung
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
            LEFT JOIN MatchScore_CTE MSC ON CV.Id_CongViec = MSC.Id_CongViec
            LEFT JOIN MatchScoreMem_CTE MSM ON CV.Id_CongViec = MSM.Id_CongViec
            WHERE 
                (@NganhNghe = '' OR NGN.Ten_NganhNghe IN (SELECT value FROM STRING_SPLIT(@NganhNghe, ','))) 
                AND (@ChuyenNganh = '' OR CN.Ten_ChuyenNganh IN (SELECT value FROM STRING_SPLIT(@ChuyenNganh, ','))) 
                AND (@ViTri = '' OR VT.Ten_ViTri IN (SELECT value FROM STRING_SPLIT(@ViTri, ','))) 
                AND (@TinhTP = '' OR TTP.Ten_TinhTP IN (SELECT value FROM STRING_SPLIT(@TinhTP, ','))) 
                AND (@QuanHuyen = '' OR QH.Ten_QuanHuyen IN (SELECT value FROM STRING_SPLIT(@QuanHuyen, ','))) 
                AND (@PhuongXa = '' OR PX.Ten_PhuongXa IN (SELECT value FROM STRING_SPLIT(@PhuongXa, ','))) 
                AND (@CapBac = '' OR CB.Ten_CapBac IN (SELECT value FROM STRING_SPLIT(@CapBac, ','))) 
                AND (@TrinhDo = '' OR TD.Ten_TrinhDo IN (SELECT value FROM STRING_SPLIT(@TrinhDo, ','))) 
                AND (@ChuyenMon = '' OR CM.Ten_ChuyenMon IN (SELECT value FROM STRING_SPLIT(@ChuyenMon, ','))) 
                AND (@NgoaiNgu = '' OR NN.Ten_NgoaiNgu IN (SELECT value FROM STRING_SPLIT(@NgoaiNgu, ','))) 
                AND (@GioiTinh = '' OR CV.GioiTinh_CongViec = @GioiTinh)
                AND (@KinhNghiem IS NULL OR CV.KinhNghiem_CongViec >= @KinhNghiem)
                AND (@MucLuongMin IS NULL OR CV.MucLuong_CongViec >= @MucLuongMin)
                AND (@MucLuongMax IS NULL OR CV.MucLuong_CongViec <= @MucLuongMax)
                AND (@DoTuoiMin IS NULL OR CV.DoTuoi_CongViec >= @DoTuoiMin)
                AND (@DoTuoiMax IS NULL OR CV.DoTuoi_CongViec <= @DoTuoiMax)
            ORDER BY MatchScore DESC;
        """)
        #print("FILTERS:", filters)
        #print("SQL:", query)
        result = session.execute(query, filters)

        #print("RESULT KEYS:", result.keys())

        # ✅ Trả lại toàn bộ thông tin của mỗi công việc
        jobs = [dict(zip(result.keys(), row)) for row in result.fetchall()]

        # 🖨️ In từng job xuống dòng cho dễ nhìn
        # print("JOBS FOUND:")
        # for job in jobs:
        #     print(job)

        # 🔁 Trả về danh sách chỉ gồm ID công việc
        job_ids = [job["Id_CongViec"] for job in jobs]
        return job_ids


    except Exception as e:
        return {"error": str(e)}

    finally:
        session.close()
