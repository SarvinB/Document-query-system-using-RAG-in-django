from langchain_community.vectorstores import FAISS
from django.conf import settings

import os


DB_PATH = str(settings.BASE_DIR / "faiss_index")


def get_vectorstore(embedding_model):

    index_file = os.path.join(DB_PATH, "index.faiss")

    if os.path.exists(index_file):
        return FAISS.load_local(
            DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    vectorstore = FAISS.from_texts(
        texts=["initial"],
        embedding=embedding_model
    )

    vectorstore.save_local(DB_PATH)

    return vectorstore

def update_chunks(texts, embedding_model, metadatas=None):

    vectorstore = get_vectorstore(embedding_model)

    if vectorstore is None:

        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embedding_model,
            metadatas=metadatas
        )

    else:

        vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )

    vectorstore.save_local(DB_PATH)

    return vectorstore
