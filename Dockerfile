# Use slim Python base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default run command
CMD ["python", "extractor.py", "sample_datasets/pdfs", "sample_datasets/outputs"]
