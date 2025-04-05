FROM python:3.10-slim

WORKDIR /app

COPY . .
# COPY requirements.txt .

# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# COPY src/ src/
COPY ../..config/ services/config/

# COPY mock_backend.py .

CMD ["uvicorn", "mock_backend:app", "--host", "0.0.0.0", "--port", "8000"]