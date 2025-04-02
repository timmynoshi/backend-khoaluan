from flask import Flask, request, jsonify
from services.job_service import get_jobs_by_filters
from services.recommend_service import recommend_jobs_by_tfidf
from services.job_detail_service import get_job_details_by_ids
from chatbot.chat_service import handle_chat
from flask_cors import CORS

from frontend.auth import login_user
from frontend.ungvien import get_thong_tin_ung_vien, update_ung_vien, get_danh_sach_ung_vien, add_ung_vien, delete_ung_vien
from frontend.diachi import get_tinhtp, get_quanhuyen, get_phuongxa, get_full_diachi
from frontend.congty import get_danh_sach_cong_ty, add_cong_ty,update_cong_ty, delete_cong_ty
from frontend.taikhoan import register_tai_khoan



app = Flask(__name__)
CORS(app)

#------------------
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
    print("🧪 Filter nhận vào:")
    for k, v in filters.items():
        print(f"  - {k}: {v}")

    jobs = get_jobs_by_filters(id_ungvien, filters)
    job_details = get_job_details_by_ids(jobs)
    return jsonify(job_details)

#------------------
@app.route("/goi-y-viec-lam", methods=["POST"])
def recommend_jobs():
    data = request.json
    id_ungvien = data.get("id_ungvien", "")
    results = recommend_jobs_by_tfidf(id_ungvien)
    job_details = get_job_details_by_ids(results)
    return jsonify(job_details)
#------------------
@app.route("/chat", methods=["POST"])
def chat_with_bot():
    data = request.json

    id_ungvien = data.get("id_ungvien")
    message = data.get("message")

    if not id_ungvien or not message:
        return jsonify({"error": "Thiếu id_ungvien hoặc message"}), 400

    response = handle_chat(id_ungvien, message)

    return jsonify({"response": response})
#------------------
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    return jsonify(login_user(data['tai_khoan'], data['mat_khau']))


@app.route('/api/ungvien/<id>', methods=['GET'])
def api_thong_tin_ung_vien(id):
    return jsonify(get_thong_tin_ung_vien(id))

@app.route('/api/ungvien/<id>', methods=['PUT'])
def api_update_ungvien(id):
    data = request.json
    return jsonify(update_ung_vien(id, data))
#-----------------------------\
@app.route('/api/tinhtp', methods=['GET'])
def api_get_tinhtp():
    return jsonify(get_tinhtp())

@app.route('/api/quanhuyen/<id_tinh>', methods=['GET'])
def api_get_quanhuyen(id_tinh):
    return jsonify(get_quanhuyen(id_tinh))

@app.route('/api/phuongxa/<id_quan>', methods=['GET'])
def api_get_phuongxa(id_quan):
    return jsonify(get_phuongxa(id_quan))
#-----------------------------------
@app.route('/api/ungvien', methods=['GET'])
def api_get_danh_sach_ungvien():
    return jsonify(get_danh_sach_ung_vien())

@app.route('/api/ungvien/<id>', methods=['DELETE'])
def api_delete_ungvien(id):
    return jsonify(delete_ung_vien(id))

@app.route('/api/ungvien', methods=['POST'])
def api_add_ungvien():
    data = request.json
    return jsonify(add_ung_vien(data))

@app.route('/api/phuongxa/<id_px>/full', methods=['GET'])
def api_get_full_diachi(id_px):
    return jsonify(get_full_diachi(id_px))

#--------------------------
@app.route('/api/congty', methods=['GET'])
def api_get_cong_ty():
    return jsonify(get_danh_sach_cong_ty())

@app.route('/api/congty', methods=['POST'])
def api_add_cong_ty():
    return jsonify(add_cong_ty(request.json))

@app.route('/api/congty/<id>', methods=['PUT'])
def api_update_cong_ty(id):
    return jsonify(update_cong_ty(id, request.json))

@app.route('/api/congty/<id>', methods=['DELETE'])
def api_delete_cong_ty(id):
    return jsonify(delete_cong_ty(id))

#------------------------
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    return jsonify(register_tai_khoan(data))
#--------------------------------
from frontend.filters import (
    get_nganhnghe, get_chuyennganh, get_vitri, get_tinhtpp,
    get_quanhuyenn, get_phuongxaa, get_trinhdo, get_capbac,
    get_kynang, get_kynangmem, get_chuyenmon, get_ngoaingu
)

@app.route('/api/nganhnghe', methods=['GET'])
def api_get_nganhnghe():
    data = get_nganhnghe()
    return jsonify(data)

@app.route('/api/chuyennganh/<id_nganh>', methods=['GET'])
def api_get_chuyennganh(id_nganh):
    return jsonify(get_chuyennganh(id_nganh))

@app.route('/api/vitri/<id_cn>', methods=['GET'])
def api_get_vitri(id_cn):
    return jsonify(get_vitri(id_cn))

@app.route('/api/tinhtpp', methods=['GET'])
def api_get_tinhtpp():
    return jsonify(get_tinhtpp())

@app.route('/api/quanhuyenn/<id_tinh>', methods=['GET'])
def api_get_quanhuyenn(id_tinh):
    return jsonify(get_quanhuyenn(id_tinh))

@app.route('/api/phuongxaa/<id_quan>', methods=['GET'])
def api_get_phuongxaa(id_quan):
    return jsonify(get_phuongxaa(id_quan))

@app.route('/api/trinhdo', methods=['GET'])
def api_get_trinhdo():
    return jsonify(get_trinhdo())

@app.route('/api/capbac', methods=['GET'])
def api_get_capbac():
    return jsonify(get_capbac())

@app.route('/api/kynang', methods=['GET'])
def api_get_kynang():
    return jsonify(get_kynang())

@app.route('/api/kynangmem', methods=['GET'])
def api_get_kynangmem():
    return jsonify(get_kynangmem())

@app.route('/api/chuyenmon', methods=['GET'])
def api_get_chuyenmon():
    return jsonify(get_chuyenmon())

@app.route('/api/ngoaingu', methods=['GET'])
def api_get_ngoaingu():
    return jsonify(get_ngoaingu())





if __name__ == "__main__":
    app.run(debug=True)
#--------------------------
