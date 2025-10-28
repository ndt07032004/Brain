from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Import từ các tệp khác trong dự án
from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt
from config import settings

class ChatbotService:
    def __init__(self):
        print("--- Khởi tạo Chatbot Service (Bộ não RAG) ---")
        self.embeddings = download_hugging_face_embeddings()
        self.retriever = self._load_vector_db()
        self.rag_chain = self._create_rag_chain()
        print("--- Chatbot Service đã sẵn sàng ---")

    def _load_vector_db(self):
        """Tải cơ sở dữ liệu Chroma đã lưu."""
        print(f"Đang tải cơ sở dữ liệu ChromaDB từ: {settings.PERSIST_DIRECTORY}...")
        try:
            vectordb = Chroma(
                persist_directory=settings.PERSIST_DIRECTORY,
                embedding_function=self.embeddings
            )
            retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            print("Tải ChromaDB và tạo retriever thành công.")
            return retriever
        except Exception as e:
            print(f"LỖI NGHIÊM TRỌNG: Không thể tải ChromaDB từ '{settings.PERSIST_DIRECTORY}'.")
            print("Hãy chắc chắn rằng bạn đã chạy 'python scripts/store_data_from_csv.py' trước.")
            exit()

    def _create_rag_chain(self):
        """Tạo RAG chain với LLM và Prompt."""
        print(f"Đang cấu hình mô hình LLM: {settings.LLM_MODEL_NAME}...")
        chatModel = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL_NAME,
            temperature=0.2,
            max_output_tokens=300,
            google_api_key=settings.GOOGLE_API_KEY,
            convert_system_message_to_human=True
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt), # Lấy prompt từ src/prompt.py
            ("human", "{input}")
        ])
        
        question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
        rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)
        print("Tạo RAG chain thành công.")
        return rag_chain

    def get_response(self, user_question: str) -> str:
        """Nhận câu hỏi và trả về câu trả lời từ RAG chain."""
        print(f"Đang xử lý câu hỏi: {user_question}")
        try:
            response = self.rag_chain.invoke({"input": user_question})
            answer = response.get("answer", "Xin lỗi, tôi không thể tìm thấy câu trả lời.")
            print(f"Đã tạo câu trả lời.")
            return answer
        except Exception as e:
            print(f"Lỗi khi xử lý câu hỏi: {e}")
            return "Đã có lỗi xảy ra trong quá trình xử lý."

# Khởi tạo một đối tượng service duy nhất khi ứng dụng bắt đầu
# Điều này đảm bảo mô hình và DB chỉ được tải 1 lần
chatbot_service = ChatbotService()