# Use lightweight official Python image
FROM python:3.11-slim

# Set system env configs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set active working directory inside container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy over requirements file first to exploit Docker build cache layers
COPY requirements.txt .

# Install dependencies directly to system scope inside container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of code into container
COPY . .

# Expose standard Streamlit communication port
EXPOSE 8501

# Run app through module layer
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
