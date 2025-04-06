FROM python:3.10-slim

WORKDIR /app

# # Set environment
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Install dependencies
# Copiando os arquivos a partir da RAIZ do projeto
COPY services/frontend/tests/requirements.txt .

# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY services/frontend/tests/ .

COPY services/config/ services/config/

# COPY mock_backend.py .

CMD ["uvicorn", "mock_backend:app", "--host", "0.0.0.0", "--port", "8000"]