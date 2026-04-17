# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install to a specific folder so we can copy it easily
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy ONLY the installed libraries from the builder stage
COPY --from=builder /install /usr/local
# Copy your actual project code
COPY . .

# Environment settings
ENV PYTHONUNBUFFERED=1
EXPOSE 7860

# Use the explicit 'python -m' call to be 100% safe
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]