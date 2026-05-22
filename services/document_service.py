from docx import Document as DocxDocument

from apps.documents.models import Document, DocumentChunk

from apps.rag.embeddings import get_embedding_model
from apps.rag.vectorstore import get_vectorstore, update_chunks

from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

from langchain_community.vectorstores import FAISS


class DocumentService:

    @staticmethod
    def extract_text(file_path: str) -> str:
        doc = DocxDocument(file_path)

        paragraphs = [
            p.text for p in doc.paragraphs
            if p.text.strip()
        ]

        return "\n".join(paragraphs)

    @staticmethod
    def split_text(text: str):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

        return splitter.split_text(text)

    @classmethod
    def process_document(cls, document: Document):

        # 1. Extract text
        text = cls.extract_text(document.file.path)

        document.content = text
        document.save()

        # 2. Chunk
        chunks = cls.split_text(text)

        # 3. Embedding model
        embedding_model = get_embedding_model()

        # 5. Save chunks
        chunk_objects = []

        for idx, chunk_text in enumerate(chunks):

            chunk = DocumentChunk.objects.create(
                document=document,
                chunk_index=idx,
                content=chunk_text
            )

            chunk_objects.append(chunk)

        # 6. Add to vector DB
        texts = [c.content for c in chunk_objects]

        metadatas = [
            {
                "document_id": c.document.id,
                "chunk_id": c.id,
                "chunk_index": c.chunk_index,
            }
            for c in chunk_objects
        ]

        # 4. Vector store
        vectorstore = update_chunks(
            texts=chunks,
            embedding_model=embedding_model,
            metadatas=metadatas
        )

        vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )

        return document
    
    def rebuild_vectorstore(embedding_model):

        all_docs = Document.objects.all()

        texts = []
        metadatas = []
        ids = []
        
        try:

            for doc in all_docs:
                chunks = DocumentChunk.objects.filter(document=doc)

                for chunk in chunks:
                    texts.append(chunk.content)
                    metadatas.append({
                        "doc_id": str(doc.id),
                        "chunk_id": chunk.chunk_index
                    })
                    ids.append(f"{doc.id}_{chunk.chunk_index}")
                    
        except Exception as e:
            error_text = str(e)
            print(error_text) 
            

        # ⚠️ handle empty DB safely
        if not texts:

            # create minimal empty index safely
            dummy_text = ["init"]
            vectorstore = FAISS.from_texts(
                dummy_text,
                embedding_model,
                metadatas=[{"init": True}],
                ids=["init"]
            )

            vectorstore.save_local("faiss_index")
            return vectorstore

        # normal case
        vectorstore = FAISS.from_texts(
            texts,
            embedding_model,
            metadatas=metadatas,
            ids=ids
        )

        vectorstore.save_local("faiss_index")

        return vectorstore

    @staticmethod
    def delete_document(document_id: int):

        embedding_model = get_embedding_model()

        # 1. delete document from DB first
        Document.objects.filter(id=document_id).delete()

        # 2. rebuild entire vectorstore
        DocumentService.rebuild_vectorstore(embedding_model)
        
    @classmethod
    def update_document(cls, document):
        """
        Rebuild everything when document is edited.
        
        """
        DocumentChunk.objects.filter(document=document).delete()
        
        new_chunks = cls.split_text(document.content)
        
        for idx, chunk_text in enumerate(new_chunks):
            DocumentChunk.objects.create(
                document=document,
                chunk_index=idx,
                content=chunk_text
            )
            
        embedding_model = get_embedding_model()
        
        try:
            DocumentService.rebuild_vectorstore(embedding_model)         
        except Exception as e:
            error_text = str(e)
            print(error_text) 