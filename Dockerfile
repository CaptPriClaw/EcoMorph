# Dockerfile

# --- Stage 1: Build Stage ---
# Use a full Python image to build our dependencies
FROM python:3.11 as builder

# Set the working directory in the container
WORKDIR /app

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate the virtual environment for subsequent commands
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies into the virtual environment
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Stage ---
# Use a smaller, "slim" image for the final container to reduce size
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment with the installed packages from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the backend application code
COPY ./backend ./backend

# Copy the ML services code, as the backend depends on it
COPY ./ml-services ./ml-services

# Expose the port the app runs on
EXPOSE 8000

# The command to run when the container starts
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]