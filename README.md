## Document-query-system-using-RAG-in-django
This project is a Django-based Document Question Answering System using Retrieval-Augmented Generation (RAG).

Features:

    Upload .docx documents
    Chunking + embeddings
    FAISS vector search
    Question answering using LangChain
    Django Admin support
    REST APIs using Django REST Framework
    Dockerized environment

# WITH DOCKER
* Because of Internet problems I couldn't test docker version

1. docker compose build
2. docker compose up
3. Project will start at: http://127.0.0.1:8000
4. Open another terminal and run:
    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py createsuperuser
Open: http://127.0.0.1:8000/admin/

# WITHOUT DOCKER

1. python manage.py makemigration
2. python manage.py migrate
3. python manage.py createsuperuser
4. python manage.py runserver

# API ENDPOINTS

ADD FILE
curl -X POST http://127.0.0.1:8000/api/documents/ \
  -F "title=file_name" \
  -F "file=@file_path"

EDITE FILE
curl -X PATCH http://127.0.0.1:8000/api/documents/file_slug/ \                      
  -F "title=file_name" \
  -F "content=edited_text"

DELETE FILE
curl -X DELETE http://127.0.0.1:8000/api/documents/file_slug/

QUESTION
curl -X POST http://127.0.0.1:8000/api/ask/ \      
  -H "Content-Type: application/json" \
  -d '{"question":"question_content"}' 

# NOTES
* Uploaded files are stored in media/
* FAISS vector index is stored in faiss_index/
