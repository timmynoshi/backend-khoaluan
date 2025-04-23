# rate.py – v5 (scenario‑based, 2 mandatory + 1 optional rule)
"""
Standalone evaluation for Job‑Recommendation project.

✔ Ground‑truth rule (recommended for small dataset):
    • Mandatory 1  – ViTri exact match
    • Mandatory 2  – Ten_TinhTP ∈ scenario.TinhTP
    • Optional +1 – Kỹ năng: >=1 keyword trùng  *hoặc*  Lương >= MucLuongMin

   A job is **correct** when it satisfies both mandatory criteria *and* at
   least one optional criterion – giving `match_score >= 3`.

✔ Dynamic‑K
    truth_size ≤ 3  ➜ K = 5
    truth_size ≤ 6  ➜ K = 8
    else           ➜ K = 10

Run:
    python rate.py
"""

from database import SessionLocal
from sqlalchemy import text
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
# ----------------------
# 1. Manual scenarios (8)
DEFAULT_SCENARIOS = [
    {
        "uid": "SCN01",
        "ViTri": "Backend Developer",
        "TinhTP": ["Hồ Chí Minh"],
        "KyNang": ["Java", "SQL"],
        "MucLuongMin": 12000000,
    },
    {
        "uid": "SCN02",
        "ViTri": "Fullstack Developer",
        "TinhTP": ["Hồ Chí Minh"],
        "KyNang": ["React", "JavaScript"],
        "MucLuongMin": 10000000,
    },
    {
        "uid": "SCN03",
        "ViTri": "Mobile Developer",
        "TinhTP": ["Hồ Chí Minh"],
        "KyNang": ["Java", "Android Studio"],
        "MucLuongMin": 15000000,
    },
    {
        "uid": "SCN04",
        "ViTri": "Data Analyst",
        "TinhTP": ["Hà Nội"],
        "KyNang": ["Python", "SQL"],
        "MucLuongMin": 10000000,
    },
    {
        "uid": "SCN05",
        "ViTri": "AI Engineer",
        "TinhTP": ["Đà Nẵng"],
        "KyNang": ["Python", "Cloud"],
        "MucLuongMin": 22000000,
    },
    {
        "uid": "SCN06",
        "ViTri": "Thợ cơ khí",
        "TinhTP": ["Hà Nội"],
        "KyNang": ["Microsoft 365"],
        "MucLuongMin": 8000000,
    },
    {
        "uid": "SCN07",
        "ViTri": "Thợ điện",
        "TinhTP": ["Hồ Chí Minh"],
        "KyNang": ["Microsoft 365"],
        "MucLuongMin": 8000000,
    },
    {
        "uid": "SCN08",
        "ViTri": "Huấn luyện viên Thể hình",
        "TinhTP": ["Hồ Chí Minh"],
        "KyNang": ["Microsoft 365"],
        "MucLuongMin": 10000000,
    },
]

# ----------------------
# 2. Load job data (title + vị trí + tỉnh + kỹ năng)
SQL_JOBS = """
SELECT CV.Id_CongViec, VT.Ten_ViTri, TP.Ten_TinhTP,
       CV.Ten_CongViec, CV.MucLuong_CongViec,
       ISNULL(KN.DanhSachKyNang,'') AS KyNang
FROM   CongViec CV
 JOIN ViTriChuyenMon VT ON CV.ViTri_CongViec = VT.Id_ViTri
 JOIN PhuongXa PX  ON CV.KhuVuc_CongViec = PX.Id_PhuongXa
 JOIN QuanHuyen QH ON PX.Id_QuanHuyen    = QH.Id_QuanHuyen
 JOIN TinhTP   TP  ON QH.Id_TinhTP       = TP.Id_TinhTP
 LEFT JOIN (
   SELECT Id_CongViec, STRING_AGG(KN.Ten_KyNang, ', ') AS DanhSachKyNang
   FROM   ChiTietKyNang CTK JOIN KyNang KN ON CTK.Id_KyNang = KN.Id_KyNang
   GROUP  BY Id_CongViec
 ) KN ON CV.Id_CongViec = KN.Id_CongViec
"""

def load_jobs():
    session = SessionLocal()
    df = pd.read_sql(text(SQL_JOBS), session.bind)
    session.close()
    return df

jobs_df = load_jobs()

# ----------------------
# 3. TF‑IDF recommender
vectorizer = TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True)
corpus = (jobs_df["Ten_CongViec"] + " " + jobs_df["Ten_ViTri"] + " " +
          jobs_df["Ten_TinhTP"]  + " " + jobs_df["KyNang"]).tolist()
X = vectorizer.fit_transform(corpus)

def recommend_for_filter(filter_text, top_k):
    vec = vectorizer.transform([filter_text])
    sims = cosine_similarity(vec, X).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    return jobs_df.iloc[top_idx]["Id_CongViec"].tolist()

# ----------------------
# 4. Ground‑truth logic
MANDATORY_SCORE = 2  # ViTri + TinhTP
OPTIONAL_SCORE   = 1  # skills OR salary
MIN_MATCH_SCORE  = MANDATORY_SCORE + OPTIONAL_SCORE  # =3

def compute_match_score(scn, job):
    score = 0
    if scn["ViTri"] == job["Ten_ViTri"]:
        score += 1
    if job["Ten_TinhTP"] in scn["TinhTP"]:
        score += 1
    # optional (skills)
    if scn.get("KyNang"):
        if any(kw in job["KyNang"] for kw in scn["KyNang"]):
            score += 1
    # optional (salary)
    if job["MucLuong_CongViec"] >= scn.get("MucLuongMin", 0):
        score += 1
    return score

def ground_truth(scn):
    mask = jobs_df.apply(lambda j: compute_match_score(scn, j) >= MIN_MATCH_SCORE, axis=1)
    return jobs_df[mask]["Id_CongViec"].tolist()

# ----------------------
# 5. Dynamic K

def choose_k(truth_size):
    if truth_size <= 3:
        return 5
    if truth_size <= 6:
        return 8
    return 10

# ----------------------
# 6. Evaluation
from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate_scenario(scn):
    truth = ground_truth(scn)
    k = choose_k(len(truth))
    filter_text = " ".join([scn["ViTri"]] + scn["TinhTP"] + scn.get("KyNang", []))
    recs = recommend_for_filter(filter_text, k)
    y_true = [1 if job in truth else 0 for job in recs]
    ndcg = round(ndcg_at_k(y_true, k), 3)
    hits = len(set(recs) & set(truth))  # giao giữa 2 tập
    p = hits / len(recs)  # K có thể là 5 / 8 / 10
    r = hits / len(truth) if truth else 0
    f1 = 2 * p * r / (p + r) if (p + r) else 0

    return {
        "Scenario": scn["uid"], "K_used": k, "truth_size": len(truth),
        "Precision": round(p,3), "Recall": round(r,3), "F1": round(f1,3),
        "nDCG": ndcg
    }

def dcg_at_k(rel_scores, k):
    rel_scores = np.asarray(rel_scores, dtype=float)[:k]  # ✅ Dùng np.asarray thay vì np.asfarray
    if rel_scores.size:
        return rel_scores[0] + np.sum(rel_scores[1:] / np.log2(np.arange(2, rel_scores.size + 1)))
    return 0.

def ndcg_at_k(y_true, k):
    dcg = dcg_at_k(y_true, k)
    ideal = dcg_at_k(sorted(y_true, reverse=True), k)
    return dcg / ideal if ideal > 0 else 0.




def main(scenarios=DEFAULT_SCENARIOS):
    df = pd.DataFrame([evaluate_scenario(s) for s in scenarios])
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
