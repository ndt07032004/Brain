from dotenv import load_dotenv
import os

load_dotenv()

# --- API Keys ---
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("LỖI: Không tìm thấy GOOGLE_API_KEY. Vui lòng kiểm tra tệp .env")
    exit()

# --- Cấu hình mô hình ---

# NÂNG CẤP: Chuyển sang mô hình đa ngôn ngữ mạnh mẽ hơn (768 dimensions)
# Mô hình này hiểu tiếng Việt tốt hơn nhiều so với 'all-MiniLM-L6-v2'
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

LLM_MODEL_NAME = "gemini-2.5-flash"

# --- Cấu hình cơ sở dữ liệu ---
PERSIST_DIRECTORY = "chroma_db_csv"