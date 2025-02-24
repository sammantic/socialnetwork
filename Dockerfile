FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies and create a virtual environment
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first for caching purposes
COPY app/requirements.txt requirements.txt

# Install dependencies
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim AS runner

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

COPY app/ app/
COPY migrations/ migrations/
COPY alembic.ini .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
