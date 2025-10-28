from langchain_community.embeddings import HuggingFaceEmbeddings
from config import settings # Import từ tệp cấu hình

def download_hugging_face_embeddings():
    """
    Tải mô hình embeddings từ HuggingFace dựa trên tên trong settings.
    """
    print(f"Đang tải mô hình embedding: {settings.EMBEDDING_MODEL_NAME}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'} # Chạy trên CPU
    )
    print("Tải embedding thành công.")
    return embeddings