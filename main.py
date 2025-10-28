from api.server import app
from config import settings # Import để đảm bảo config được tải

if __name__ == '__main__':
    print("--- KHỞI ĐỘNG MÁY CHỦ CHATBOT (Cấu trúc mới) ---")
    print(f"API Key đã được tải: {'Có' if settings.GOOGLE_API_KEY else 'Không'}")
    print(f"Sử dụng LLM: {settings.LLM_MODEL_NAME}")
    print(f"Cơ sở dữ liệu: {settings.PERSIST_DIRECTORY}")
    
    # Chạy máy chủ Flask
    # host="0.0.0.0" cho phép các thiết bị khác trong mạng (như Unity) kết nối
    app.run(host="0.0.0.0", port=8080, debug=True)