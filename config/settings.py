from dotenv import load_dotenv
import os

# Tải các biến môi trường từ tệp .env
load_dotenv()

# --- API Keys ---
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("LỖI: Không tìm thấy GOOGLE_API_KEY. Vui lòng kiểm tra tệp .env")
    exit()

# --- Cấu hình mô hình ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # Model embedding từ HuggingFace
LLM_MODEL_NAME = "gemini-2.5-flash"       # Model Gemini (từ run.py)

# --- Cấu hình cơ sở dữ liệu ---
# Thư mục để lưu trữ cơ sở dữ liệu vector (từ test.py)
PERSIST_DIRECTORY = "chroma_db_csv"