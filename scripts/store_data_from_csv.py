import csv
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from src.helper import download_hugging_face_embeddings
from config import settings
import os
import shutil

def load_data_from_csv(filepath="dataset.csv"):
    """
    Đọc dữ liệu từ tệp CSV và tạo danh sách Documents cho LangChain.
    Logic dựa trên tệp test.py
    """
    documents = []
    print(f"Đang đọc tệp {filepath}...")
    
    try:
        with open(filepath, encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader) # Bỏ qua dòng tiêu đề
            
            count = 0
            for i, line in enumerate(reader):
                if len(line) < 5: # Đảm bảo đủ 5 cột
                    print(f"Bỏ qua dòng {i+2}: không đủ cột.")
                    continue
                
                # Ghép các thông tin làm nội dung (content)
                content = (
                    f"Tên: {line[1]}. "
                    f"Đặc điểm: {line[2]}. "
                    f"Thời kỳ: {line[3]}. "
                    f"Công dụng/Ý nghĩa: {line[4]}"
                )
                
                # Tạo metadata
                metadata = {
                    "item_id": line[0],
                    "ten": line[1],
                    "thoi_ky": line[3],
                    "source": filepath
                }
                
                documents.append(Document(page_content=content, metadata=metadata))
                count += 1
                
        print(f"Đã đọc thành công {count} tài liệu từ CSV.")
        return documents
        
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy tệp {filepath}. Vui lòng kiểm tra lại.")
        return []
    except Exception as e:
        print(f"Lỗi khi đọc CSV: {e}")
        return []

def main():
    # 1. Tải dữ liệu từ CSV
    documents = load_data_from_csv("dataset.csv")
    
    if not documents:
        print("Không có dữ liệu để xử lý. Dừng lại.")
        return

    # 2. Tải mô hình embedding
    embeddings = download_hugging_face_embeddings()

    # 3. Tạo và lưu trữ vào ChromaDB
    print(f"Đang tạo và lưu trữ vector vào thư mục: '{settings.PERSIST_DIRECTORY}'...")
    
    # Xóa thư mục DB cũ nếu tồn tại để build lại từ đầu
    if os.path.exists(settings.PERSIST_DIRECTORY):
        print(f"Phát hiện thư mục cũ. Đang xóa: '{settings.PERSIST_DIRECTORY}'")
        shutil.rmtree(settings.PERSIST_DIRECTORY)

    # Tạo và lưu trữ vector
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=settings.PERSIST_DIRECTORY
    )
    
    print("--- HOÀN TẤT NẠP DỮ LIỆU VÀO CHROMA ---")

if __name__ == "__main__":
    main()