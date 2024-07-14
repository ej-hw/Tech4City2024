FROM python:3.12-slim-bullseye

WORKDIR /app

COPY frontend /app/frontend

COPY backend /app/backend

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app/backend

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
