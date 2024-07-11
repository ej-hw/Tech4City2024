# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install the necessary build tools
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container at /app
COPY backend/requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container at /app
COPY backend /app

# Copy the frontend files into the container at /app/templates
RUN mkdir -p /app/templates
COPY frontend/index.html /app/templates/index.html

# Copy static files
RUN mkdir -p /app/static
COPY frontend/styles.css /app/static/styles.css
COPY frontend/script.js /app/static/script.js

# Download NLTK data
RUN python -m nltk.downloader stopwords punkt

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
