from api.server import app
from config import settings
from utils.logger import get_logger

# Khởi tạo logger chính
logger = get_logger(__name__)

if __name__ == '__main__':
    logger.info("--- KHỞI ĐỘNG MÁY CHỦ CHATBOT ---")
    logger.info(f"API Key đã được tải: {'Có' if settings.GOOGLE_API_KEY else 'Không'}")
    logger.info(f"Sử dụng LLM: {settings.LLM_MODEL_NAME}")
    logger.info(f"Sử dụng Embedding: {settings.EMBEDDING_MODEL_NAME}")
    logger.info(f"Cơ sở dữ liệu: {settings.PERSIST_DIRECTORY}")
    
    app.run(host="0.0.0.0", port=8080, debug=True)