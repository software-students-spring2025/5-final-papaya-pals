FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY tests/ tests/

# Run tests during build
RUN python -m pytest tests/ --cov=src --cov-report=term-missing

# Create a non-root user
RUN useradd -m -r user && chown -R user:user /app
USER user

CMD ["python", "-m", "src.db"]
