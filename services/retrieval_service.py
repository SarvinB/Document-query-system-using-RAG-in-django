from apps.rag.embeddings import get_embedding_model
from apps.rag.vectorstore import get_vectorstore


class RetrievalService:

    @staticmethod
    def retrieve(question: str, k: int = 3):

        embedding_model = get_embedding_model()

        vectorstore = get_vectorstore(embedding_model)
        
        try:
            results = vectorstore.similarity_search_with_score(
                question,
                k=k
            )
            
        except Exception as e:
            error_text = str(e)
            results = []
            print(error_text) 

        formatted_results = []

        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })

        return formatted_results