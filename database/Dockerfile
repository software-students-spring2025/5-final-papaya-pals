# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Create a non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Command to run the application
CMD ["python", "-m", "src.main"]
