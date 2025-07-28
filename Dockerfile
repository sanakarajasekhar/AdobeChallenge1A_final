# FROM --platform=linux/amd64 python:3.9-slim

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY extractor.py .

# CMD ["python", "extractor.py"]



FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY extractor.py .

CMD ["python", "extractor.py"]
