# 1. Base Image
FROM python:3.13-slim

# 2. Poetry Environment Variables
ENV POETRY_VERSION=2.0.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Work Directory
WORKDIR /app
ENV PYTHONPATH=/app
# 4. System Dependencies
# Added libgomp1 for FAISS/AI library stability
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# 6. Copy ONLY dependency files (for Layer Caching)
# This step is cached unless your pyproject.toml or poetry.lock changes.
COPY pyproject.toml poetry.lock* ./

# 7. Install Dependencies
# --only main: skips development tools like pytest/black
RUN poetry install --only main --no-root

# 8. Copy Application Contents
COPY . .

# 9. Expose Ports (Streamlit: 8501, Uvicorn: 9999)
EXPOSE 8501
EXPOSE 9999

# 10. Run the app
# Using python -m ensures your main.py is the entry point
CMD ["python", "-m", "app.main"]