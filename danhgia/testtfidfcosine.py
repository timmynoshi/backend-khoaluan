from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Input từ người dùng
user_input = "Tôi muốn tìm việc làm AI Engineer, ở Bình Thạnh, Hồ Chí Minh, tôi giỏi sử dụng LLM và fine tune"

# Danh sách 5 công việc mẫu
jobs = [
    {
        "Ten_CongViec": "AI Engineer",
        "Ten_CongTy": "ABC Corp",
        "NganhNghe": "Công nghệ Thông tin",
        "ChuyenNganh": "Artificial Intelligent (AI)",
        "ViTriChuyenMon": "AI Engineer",
        "PhuongXa": "Phường 25",
        "QuanHuyen": "Bình Thạnh",
        "TinhTP": "Hồ Chí Minh",
        "KyNang": ["LLM", "NLP", "Machine Learning"]
    },
    {
        "Ten_CongViec": "Data Scientist",
        "Ten_CongTy": "XYZ Ltd",
        "NganhNghe": "Công nghệ Thông tin",
        "ChuyenNganh": "Data Science",
        "ViTriChuyenMon": "Data Analyst",
        "PhuongXa": "Phường Bến Nghé",
        "QuanHuyen": "Quận 1",
        "TinhTP": "Hồ Chí Minh",
        "KyNang": ["Python", "Data Analysis", "SQL"]
    },
    {
        "Ten_CongViec": "Backend Developer",
        "Ten_CongTy": "DEF Co",
        "NganhNghe": "Công nghệ Thông tin",
        "ChuyenNganh": "Software Engineering",
        "ViTriChuyenMon": "Backend Developer",
        "PhuongXa": "Phường 26",
        "QuanHuyen": "Bình Thạnh",
        "TinhTP": "Hồ Chí Minh",
        "KyNang": ["Node.js", "SQL", "REST API"]
    },
    {
        "Ten_CongViec": "Machine Learning Engineer",
        "Ten_CongTy": "GHI Tech",
        "NganhNghe": "Công nghệ Thông tin",
        "ChuyenNganh": "Artificial Intelligent (AI)",
        "ViTriChuyenMon": "AI Engineer",
        "PhuongXa": "Phường 6",
        "QuanHuyen": "Quận 3",
        "TinhTP": "Hồ Chí Minh",
        "KyNang": ["Fine-tuning", "LLM", "Deep Learning"]
    },
    {
        "Ten_CongViec": "Frontend Developer",
        "Ten_CongTy": "KLM Studio",
        "NganhNghe": "Công nghệ Thông tin",
        "ChuyenNganh": "Software Engineering",
        "ViTriChuyenMon": "Frontend Developer",
        "PhuongXa": "Phường Tân Hưng",
        "QuanHuyen": "Quận 7",
        "TinhTP": "Hồ Chí Minh",
        "KyNang": ["React", "JavaScript", "HTML", "CSS"]
    }
]
def build_job_text(job):
    return (
        f"Tên công việc: {job['Ten_CongViec']}. "
        f"Ngành nghề: {job['NganhNghe']}. "
        f"Chuyên ngành: {job['ChuyenNganh']}. "
        f"Vị trí chuyên môn: {job['ViTriChuyenMon']}. "
        f"Địa điểm: {job['PhuongXa']}, {job['QuanHuyen']}, {job['TinhTP']}. "
        f"Kỹ năng: {', '.join(job['KyNang'])}."
    )
# Tạo danh sách văn bản: input người dùng + mô tả công việc
documents = [user_input] + [build_job_text(job) for job in jobs]

# Vector hóa TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Debug: in ra các từ đã được chọn bởi TF-IDF
print("📌 Từ khóa TF-IDF (vocabulary):")
print(vectorizer.get_feature_names_out())

# Debug: in vector TF-IDF của người dùng
print("\n🧠 Vector TF-IDF của input người dùng:")
user_vector = tfidf_matrix[0].toarray()[0]
for idx, val in enumerate(user_vector):
    if val > 0:
        word = vectorizer.get_feature_names_out()[idx]
        print(f"{word}: {val:.4f}")


# In vector TF-IDF của người dùng
print("\n📥 Vector TF-IDF của người dùng (dạng list):")
print(tfidf_matrix[0].toarray()[0].tolist())

# In vector TF-IDF của từng công việc
print("\n📋 Vector TF-IDF của từng công việc (dạng list):")
for i, job in enumerate(jobs):
    vector = tfidf_matrix[i + 1].toarray()[0].tolist()
    print(f"{job['Ten_CongViec']} ({job['Ten_CongTy']}):")
    print(vector)


# Tính cosine similarity giữa input và từng mô tả công việc
similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

# Tạo bảng kết quả
# Kết quả
results = []
for i, job in enumerate(jobs):
    results.append({
        "Công việc": job["Ten_CongViec"],
        "Công ty": job["Ten_CongTy"],
        "Địa điểm": f"{job['PhuongXa']}, {job['QuanHuyen']}, {job['TinhTP']}",
        "Kỹ năng": ", ".join(job["KyNang"]),
        "Điểm khớp (Cosine)": round(similarities[i], 4)
    })

# Xuất kết quả
df_results = pd.DataFrame(results).sort_values(by="Điểm khớp (Cosine)", ascending=False)
print("\n📊 Kết quả gợi ý công việc:")
print(df_results.to_string(index=False))
