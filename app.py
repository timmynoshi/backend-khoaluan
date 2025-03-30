from flask import Flask, request, jsonify
from services.job_service import get_jobs_by_filters
from services.recommend_service import recommend_jobs_by_tfidf
from services.job_detail_service import get_job_details_by_ids
from chatbot.chat_service import handle_chat

app = Flask(__name__)

@app.route("/get_jobs", methods=["POST"])
def get_jobs():
    data = request.json

    # Lấy ID ứng viên & bộ lọc từ request
    id_ungvien = data.get("id_ungvien", "")

    filters = {
        "ViTri": data.get("ViTri", ""),
        "ChuyenNganh": data.get("ChuyenNganh", ""),
        "NganhNghe": data.get("NganhNghe", ""),
        "PhuongXa": data.get("PhuongXa", ""),
        "QuanHuyen": data.get("QuanHuyen", ""),
        "TinhTP": data.get("TinhTP", ""),
        "CapBac": data.get("CapBac", ""),
        "TrinhDo": data.get("TrinhDo", ""),
        "ChuyenMon": data.get("ChuyenMon", ""),
        "NgoaiNgu": data.get("NgoaiNgu", ""),
        "KyNang": data.get("KyNang", ""),
        "KyNangMem": data.get("KyNangMem", ""),
        "MucLuongMin": data.get("MucLuongMin", None),
        "MucLuongMax": data.get("MucLuongMax", None),
        "DoTuoiMin": data.get("DoTuoiMin", None),
        "DoTuoiMax": data.get("DoTuoiMax", None),
        "GioiTinh": data.get("GioiTinh", None),
        "KinhNghiem": data.get("KinhNghiem", None),
    }

    jobs = get_jobs_by_filters(id_ungvien, filters)
    job_details = get_job_details_by_ids(jobs)
    return jsonify(job_details)


@app.route("/goi-y-viec-lam", methods=["POST"])
def recommend_jobs():
    data = request.json
    id_ungvien = data.get("id_ungvien", "")
    results = recommend_jobs_by_tfidf(id_ungvien)
    job_details = get_job_details_by_ids(results)
    return jsonify(job_details)

@app.route("/chat", methods=["POST"])
def chat_with_bot():
    data = request.json

    id_ungvien = data.get("id_ungvien")
    message = data.get("message")

    if not id_ungvien or not message:
        return jsonify({"error": "Thiếu id_ungvien hoặc message"}), 400

    response = handle_chat(id_ungvien, message)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
