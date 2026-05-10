# Pakai komputer Linux dengan Python 3.12 (Sesuai yang ada di laptop)
FROM python:3.12-slim

# Buat folder kerja di dalam cloud
WORKDIR /app

# Mengajari Cloud untuk meng-install aplikasi Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean

# Copy daftar library dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file kodinganmu ke dalam cloud
COPY . .

# Nyalakan FastAPI di port 7860 (Port wajib dari Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]