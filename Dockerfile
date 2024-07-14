FROM python:3.11.9-slim AS base

WORKDIR /app
COPY ./backend/ .
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
ENV FORCE_CMAKE=1
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential cmake libopenblas-dev libgomp1
RUN pip install --user -r requirements.txt
RUN apt-get purge -y --auto-remove cmake
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

ENV HF_HOME=/app
COPY ./frontend frontend
EXPOSE 80
CMD ["python", "app.py"]
