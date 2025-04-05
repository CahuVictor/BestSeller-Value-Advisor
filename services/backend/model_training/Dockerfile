FROM python:3.10-slim

WORKDIR /app
COPY ../requirements-model.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python", "train.py"]
