FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install -i https://mirror-pypi.runflare.com/simple --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create media + faiss folders
RUN mkdir -p /app/media /app/faiss_index

# Expose port
EXPOSE 8000

# Run Django with gunicorn (production-ready)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]