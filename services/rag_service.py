from langchain_openai import ChatOpenAI

from apps.qa.models import QuestionAnswerHistory

from services.retrieval_service import RetrievalService

import os

from langchain.chat_models import init_chat_model

from openai import OpenAI

class RagService:

    def __init__(self):
        
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        
        self.llm = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            )

    def ask(self, question: str):

        retrieved = RetrievalService.retrieve(question)

        context = "\n\n".join([
            r["content"] for r in retrieved
        ])

        prompt = f"""
Answer ONLY from the provided context.

Context:
{context}

Question:
{question}

If answer is not found say:
"Not found in documents."
"""

        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
            {
                "role": "user",
                "content": prompt
            }
            ],
            extra_body={"reasoning": {"enabled": True}}
        )

        response = response.choices[0].message

        history = QuestionAnswerHistory.objects.create(
            question=question,
            answer=response.content,
            retrieved_chunks=retrieved
        )

        return {
            "answer": response.content,
            "sources": [
                r["metadata"]
                for r in retrieved
            ],
            "retrieved_chunks": retrieved,
            "history_id": history.id
        }