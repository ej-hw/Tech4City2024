# Stage 1: Build frontend with Nginx
FROM nginx:1.10.1-alpine AS frontend

# Copy the frontend files to the Nginx HTML directory
COPY frontend /usr/share/nginx/html

# Stage 2: Build backend with Python
FROM python:3.10-slim AS backend

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY backend/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY backend /app

# Ensure the VADER lexicon is downloaded
RUN python -m nltk.downloader vader_lexicon

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Expose port 8000 for the Flask app
EXPOSE 8000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
