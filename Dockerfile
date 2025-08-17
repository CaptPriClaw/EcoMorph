# Dockerfile (Corrected and Simplified)

# Use a slim Python image as our base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set the PYTHONPATH environment variable so Python can find your modules
ENV PYTHONPATH=/app

# --- Step 1: Install Dependencies ---
# Copy requirements.txt FIRST to leverage Docker's build cache.
COPY requirements.txt .
# NOW, run pip install with the file present.
RUN pip install --no-cache-dir -r requirements.txt

# --- Step 2: Download NLTK Data ---
# Copy the scripts folder which contains the downloader
COPY ./scripts ./scripts
# Run the download script
RUN python scripts/download_nltk_data.py

# --- Step 3: Copy All Application Code ---
# This single command copies your backend, ml-services, etc., into the container
COPY . .

# --- Step 4: Run the Application ---
# Expose the port the app runs on
EXPOSE 8000

# The command to run when the container starts
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]