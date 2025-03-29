from sqlalchemy import text
from database import SessionLocal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs_by_tfidf(id_ungvien, top_n=5):
    session = SessionLocal()
    try:
        # B1: Lấy 5 log tìm kiếm gần nhất từ bảng FilterUV của ứng viên
        query_log = text("""
            SELECT TOP 5 * FROM FilterUV
            WHERE Id_UngVien = :id_ungvien
            ORDER BY ThoiGian DESC
        """)
        filters = session.execute(query_log, {"id_ungvien": id_ungvien}).fetchall()
        if not filters:
            return []

        # Các trường mô tả hành vi tìm kiếm
        important_fields = [
            "ViTri", "ChuyenNganh", "NganhNghe",
            "CapBac", "TrinhDo", "ChuyenMon",
            "NgoaiNgu", "KyNang", "KyNangMem",
            "QuanHuyen", "TinhTP"
        ]

        # Trọng số theo thời gian (log mới hơn ưu tiên hơn)
        weights = [1.0, 0.8, 0.6, 0.4, 0.2]
        filter_weighted_parts = []
        target_tinhtp = set()

        for i, row in enumerate(filters):
            row_dict = dict(row._mapping)
            text_content = " ".join(str(row_dict[col]).strip() for col in important_fields if col in row_dict and row_dict[col])
            weight = weights[i] if i < len(weights) else 0.2
            multiplier = int(weight * 5)
            weighted_text = (text_content + " ") * multiplier
            filter_weighted_parts.append(weighted_text.strip())

            # Lưu tỉnh/thành để lọc job theo vùng
            if "TinhTP" in row_dict and row_dict["TinhTP"]:
                for tp in row_dict["TinhTP"].split(","):
                    target_tinhtp.add(tp.strip())

        filter_text = " ".join(filter_weighted_parts)
        if not filter_text.strip():
            return {"error": "Không có đủ thông tin tìm kiếm để gợi ý."}

        # B2: Truy vấn công việc (chỉ lấy tên mô tả, không lấy ID)
        query_jobs = text("""
            SELECT 
                CV.Id_CongViec, CV.Ten_CongViec,
                CV.MucLuong_CongViec, CV.DoTuoi_CongViec,
                CV.KinhNghiem_CongViec, CV.GioiTinh_CongViec,

                NTD.Ten_NhaTuyenDung,
                VT.Ten_ViTri, CB.Ten_CapBac, TD.Ten_TrinhDo, 
                CM.Ten_ChuyenMon, NN.Ten_NgoaiNgu,
                ISNULL(KN.DanhSachKyNang, '') AS KyNang,
                ISNULL(KNM.DanhSachKyNangMem, '') AS KyNangMem,
                QH.Ten_QuanHuyen, TTP.Ten_TinhTP

            FROM CongViec CV
            JOIN NhaTuyenDung NTD ON CV.Id_NhaTuyenDung = NTD.Id_NhaTuyenDung
            JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri
            JOIN CapBac CB ON CV.CapBac_CongViec = CB.Id_CapBac
            JOIN TrinhDo TD ON CV.TrinhDo_CongViec = TD.Id_TrinhDo
            JOIN ChuyenMon CM ON CV.ChuyenMon_CongViec = CM.Id_ChuyenMon
            JOIN NgoaiNgu NN ON CV.NgoaiNgu_CongViec = NN.Id_NgoaiNgu
            JOIN PhuongXa PX ON CV.KhuVuc_CongViec = PX.Id_PhuongXa
            JOIN QuanHuyen QH ON PX.Id_QuanHuyen = QH.Id_QuanHuyen
            JOIN TinhTP TTP ON QH.Id_TinhTP = TTP.Id_TinhTP
            LEFT JOIN (
                SELECT Id_CongViec, STRING_AGG(Ten_KyNang, ', ') AS DanhSachKyNang
                FROM ChiTietKyNang CTK JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
                GROUP BY Id_CongViec
            ) AS KN ON CV.Id_CongViec = KN.Id_CongViec
            LEFT JOIN (
                SELECT Id_CongViec, STRING_AGG(Ten_KyNangMem, ', ') AS DanhSachKyNangMem
                FROM ChiTietKyNangMem CTKM JOIN KyNangMem KNM ON CTKM.Id_KyNangMem = KNM.Id_KyNangMem
                GROUP BY Id_CongViec
            ) AS KNM ON CV.Id_CongViec = KNM.Id_CongViec
        """)
        rows = session.execute(query_jobs).fetchall()

        jobs = []
        job_corpus = []

        for row in rows:
            row_dict = dict(row._mapping)
            text_job = " ".join(str(val).strip() for val in row_dict.values() if val is not None)
            row_dict["joined_text"] = text_job  # để tính TF-IDF
            jobs.append(row_dict)
            job_corpus.append(text_job)

        # B3: Lọc theo TinhTP nếu ứng viên có chọn vùng
        if target_tinhtp:
            jobs = [job for job in jobs if job["Ten_TinhTP"] in target_tinhtp]
            job_corpus = [job["joined_text"] for job in jobs]

        if not jobs:
            return []

        # B4: TF-IDF và tính cosine similarity
        corpus = [filter_text] + job_corpus
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        for i, sim in enumerate(similarities):
            jobs[i]["score"] = round(float(sim), 4)
            jobs[i].pop("joined_text", None)  # Xóa text nội bộ trước khi trả về

        # B5: Trả về top N job phù hợp nhất
        # ✅ Trả lại toàn bộ thông tin của mỗi công việc
        top_jobs = sorted(jobs, key=lambda x: x["score"], reverse=True)[:top_n]

        # 🖨️ In từng job xuống dòng cho dễ nhìn
        print("JOBS FOUND:")
        for job in top_jobs:
            print(job)

        # 🔁 Trả về danh sách chỉ gồm ID công việc
        job_ids = [job["Id_CongViec"] for job in top_jobs]
        return job_ids

    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()
