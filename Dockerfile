FROM python:3.13-slim

WORKDIR /app

# Install system dependencies required to build psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev

# Upgrade pip and install uv
RUN pip install --upgrade pip && pip install uv

# Copy dependency and environment files
COPY pyproject.toml uv.lock .python-version .env ./

# Copy the src directory
COPY src ./src

# Install dependencies into the virtual environment
RUN uv sync

# Expose the application port
EXPOSE 3000

# Run the app
CMD [".venv/bin/python", "src/main.py"]
