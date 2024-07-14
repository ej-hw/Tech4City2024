FROM python:3.11.9-slim

WORKDIR /app
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
ENV FORCE_CMAKE=1
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake libopenblas-dev libgomp1 && \
    pip install --no-cache-dir llama-cpp-python==0.2.82 && \
    apt-get purge -y --auto-remove cmake && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --user torch==2.3.1
COPY ./backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

ENV HF_HOME=/app
COPY ./backend .
COPY ./frontend static
COPY ./backend/swagger.json ./static/swagger.json
EXPOSE 8000
CMD ["python", "app.py"]
