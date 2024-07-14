FROM python:3.11.9-slim AS base

FROM base AS dependencies
WORKDIR /app
COPY ./backend/requirements.txt .
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
ENV FORCE_CMAKE=1
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential cmake libopenblas-dev
RUN pip install --user -r requirements.txt
RUN apt-get purge -y --auto-remove cmake
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

FROM base AS runner
ENV HF_HOME=/app
WORKDIR /app
COPY --from=dependencies /root/.local /root/.local
COPY ./frontend frontend
COPY ./backend .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 80
CMD ["python", "app.py"]
