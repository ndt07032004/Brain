from flask import Flask, request, jsonify, render_template, Response

# Import đối tượng "bộ não" đã được khởi tạo
from services.chatbot_service import chatbot_service

# Cấu hình lại Flask để tìm đúng thư mục templates/static
app = Flask(__name__, static_folder='../static', template_folder='../templates') 

# === Route 1: Giao diện Web (Giữ nguyên) ===
@app.route("/")
def index():
    """
    Route này render tệp chat.html từ thư mục 'templates'.
    """
    print("Đang tải giao diện web chat.html...")
    return render_template("chat.html")

# === Route 2: API cho Web (Giữ nguyên) ===
@app.route("/get", methods=["GET", "POST"])
def chat_api_web():
    """
    API này dành cho chat.html
    Nhận Form Data, Trả về VĂN BẢN THUẦN TÚY (plain text).
    """
    msg = None
    if request.form:
        msg = request.form.get("msg")
    
    if not msg:
        # Trang web mong đợi text, nên trả lỗi text
        return Response("Lỗi: Không tìm thấy 'msg' trong request", 
                        mimetype='text/plain', status=400)

    # Gọi chung 1 bộ não
    answer = chatbot_service.get_response(msg)
    
    # Trả về VĂN BẢN cho chat.html
    return Response(answer, mimetype='text/plain')


# === Route 3: API MỚI CHO UNITY (JSON) ===
@app.route("/api/chat", methods=["GET", "POST"])
def chat_api_json():
    """
    API này dành cho Unity (LKZMuZiLi/human)
    Nhận JSON, Trả về JSON.
    """
    msg = None
    
    # API này CHỈ chấp nhận JSON
    if not request.is_json:
        return jsonify({"error": "Yêu cầu này phải là JSON."}), 415 # Unsupported Media Type

    try:
        data = request.get_json()
        msg = data.get("msg")
    except Exception as e:
        print(f"Lỗi khi đọc JSON: {e}")
        return jsonify({"error": f"Lỗi đọc JSON: {e}"}), 400

    if not msg:
        return jsonify({"error": "Không tìm thấy 'msg' trong JSON body"}), 400

    # Gọi chung 1 bộ não
    answer = chatbot_service.get_response(msg)
    
    # Trả về JSON cho Unity
    return jsonify({"answer": answer})