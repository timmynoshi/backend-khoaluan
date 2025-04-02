from langchain.agents import Tool
from services.job_detail_service import get_all_job_details

# ✅ Cập nhật tools.py sử dụng TF-IDF + cosine similarity

def recommend_jobs_tool(input_str: str) -> str:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    def build_job_text(job):
        return (
            f"Tên công việc: {job['Ten_CongViec']}. "
            f"Vị trí chuyên môn: {job['Ten_ViTri']}. "
            f"Chuyên ngành: {job['Ten_ChuyenNganh']}. "
            f"Ngành nghề: {job['Ten_NganhNghe']}. "
            f"Địa điểm: {job['Ten_QuanHuyen']}, {job['Ten_TinhTP']}. "
            f"Kỹ năng: {job['DanhSachKyNang'] or 'Không yêu cầu rõ'}. "
            f"Mức lương: {job['MucLuong_CongViec']} VND."
        )

    try:
        input_str = input_str.strip().strip("'\"")
        print(f"\n📥 Input từ người dùng: {input_str}")

        jobs = get_all_job_details()
        print(f"📊 Tổng số công việc trong hệ thống: {len(jobs)}")

        if not jobs:
            return "Hiện tại hệ thống chưa có công việc nào để gợi ý."

        job_texts = [build_job_text(job) for job in jobs]
        documents = [input_str] + job_texts

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        top_indices = similarities.argsort()[::-1][:5]
        matched = [(jobs[i], similarities[i]) for i in top_indices if similarities[i] > 0.1]

        if not matched:
            return "Rất tiếc, hiện tại tôi chưa tìm được việc làm nào phù hợp với yêu cầu bạn nêu."

        result_lines = []
        for job, score in matched:
            line = (
                f"- Tên công việc: {job['Ten_CongViec']} tại {job['Ten_CongTy']}\n"
                f"  Địa điểm: {job['Ten_QuanHuyen']}, {job['Ten_TinhTP']}\n"
                f"  Vị trí chuyên môn: {job['Ten_ViTri']}\n"
                f"  Mức lương: {job['MucLuong_CongViec']} VND\n"
                f"  Kỹ năng yêu cầu: {job['DanhSachKyNang'] or 'Không yêu cầu rõ'}\n"
                f"  Điểm khớp: {score:.2f}\n"
            )
            result_lines.append(line)

        return "### DANH_SACH_CONG_VIEC:\n" + "\n\n".join(result_lines)

    except Exception as e:
        return f"Lỗi khi gợi ý việc làm: {str(e)}"


tools = [
    Tool(
        name="GoiYViecLam",
        func=recommend_jobs_tool,
        description="Gợi ý việc làm phù hợp cho một ứng viên dựa vào ID và thông tin đầu vào (ví dụ: 'Việc làm Backend, kỹ năng Java,việc làm ở Hồ Chí Minh')"
    )
]
