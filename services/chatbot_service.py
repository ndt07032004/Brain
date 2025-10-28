from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class ChatbotService:
    def __init__(self):
        logger.info("--- Khởi tạo Chatbot Service (Bộ não RAG) ---")
        self.embeddings = download_hugging_face_embeddings()
        self.retriever = self._load_vector_db()
        self.rag_chain = self._create_rag_chain()
        logger.info("--- Chatbot Service đã sẵn sàng ---")

    def _load_vector_db(self):
        """Tải cơ sở dữ liệu Chroma đã lưu."""
        logger.info(f"Đang tải CSDL ChromaDB từ: {settings.PERSIST_DIRECTORY}...")
        try:
            vectordb = Chroma(
                persist_directory=settings.PERSIST_DIRECTORY,
                embedding_function=self.embeddings
            )
            
            # TỐI ƯU RAG: Lấy 5 kết quả (thay vì 3) để LLM có nhiều ngữ cảnh hơn
            retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            
            logger.info("Tải ChromaDB và tạo retriever (k=5) thành công.")
            return retriever
        except Exception as e:
            logger.error(f"LỖI NGHIÊM TRỌNG khi tải ChromaDB: {e}", exc_info=True)
            logger.error("Hãy chắc chắn rằng bạn đã chạy 'python -m scripts.store_data_from_csv' trước.")
            exit() # Thoát nếu không tải được DB

    def _create_rag_chain(self):
        """Tạo RAG chain với LLM và Prompt."""
        logger.info(f"Đang cấu hình mô hình LLM: {settings.LLM_MODEL_NAME}...")
        chatModel = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL_NAME,
            temperature=0.3, # Tăng nhẹ nhiệt độ để trả lời tự nhiên hơn
            max_output_tokens=500, # Tăng giới hạn token
            google_api_key=settings.GOOGLE_API_KEY,
            convert_system_message_to_human=True
        )
        
        # Sử dụng prompt đã tối ưu (nhà sử học)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
        rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)
        logger.info("Tạo RAG chain thành công.")
        return rag_chain

    def get_response(self, user_question: str) -> str:
        """Nhận câu hỏi và trả về câu trả lời từ RAG chain."""
        logger.info(f"Đang xử lý câu hỏi: {user_question}")
        try:
            response = self.rag_chain.invoke({"input": user_question})
            answer = response.get("answer", "Xin lỗi, tôi không thể tìm thấy câu trả lời.")
            logger.info(f"Đã tạo câu trả lời cho: {user_question}")
            return answer
        except Exception as e:
            logger.error(f"Lỗi khi xử lý câu hỏi '{user_question}': {e}", exc_info=True)
            return "Đã có lỗi xảy ra trong quá trình xử lý, vui lòng thử lại."

# Khởi tạo một đối tượng service duy nhất
chatbot_service = ChatbotService()