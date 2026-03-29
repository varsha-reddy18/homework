FROM python:3.11-slim

WORKDIR /code

# Install system dependencies for OCR and image processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY app/ /code/app/
COPY app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]