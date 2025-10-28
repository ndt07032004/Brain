from flask import Flask, request, jsonify, render_template, Response
from services.chatbot_service import chatbot_service
from utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__, static_folder='../static', template_folder='../templates') 

@app.route("/")
def index():
    """Route cho trang web chat.html"""
    logger.info(f"Yêu cầu GET đến trang chủ '/', render chat.html...")
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat_api_web():
    """API cho web chat.html (Nhận Form, Trả về Text)"""
    msg = None
    if request.form:
        msg = request.form.get("msg")
    
    if not msg:
        logger.warning("Yêu cầu đến /get không có 'msg' trong Form.")
        return Response("Lỗi: Không tìm thấy 'msg' trong request", 
                        mimetype='text/plain', status=400)

    logger.info(f"Yêu cầu đến /get (Web): {msg}")
    answer = chatbot_service.get_response(msg)
    return Response(answer, mimetype='text/plain')


@app.route("/api/chat", methods=["GET", "POST"])
def chat_api_json():
    """API cho Unity (Nhận JSON, Trả về JSON)"""
    if not request.is_json:
        logger.warning("Yêu cầu đến /api/chat không phải là JSON.")
        return jsonify({"error": "Yêu cầu này phải là JSON."}), 415

    try:
        data = request.get_json()
        msg = data.get("msg")
    except Exception as e:
        logger.error(f"Lỗi khi đọc JSON từ /api/chat: {e}", exc_info=True)
        return jsonify({"error": f"Lỗi đọc JSON: {e}"}), 400

    if not msg:
        logger.warning("Yêu cầu đến /api/chat không có 'msg' trong JSON.")
        return jsonify({"error": "Không tìm thấy 'msg' trong JSON body"}), 400

    logger.info(f"Yêu cầu đến /api/chat (JSON): {msg}")
    answer = chatbot_service.get_response(msg)
    return jsonify({"answer": answer})