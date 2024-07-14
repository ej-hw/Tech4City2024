# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy the requirements file into the container
COPY backend/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the YOLO files into the container
COPY backend/yolov3.cfg backend/yolov3.weights backend/coco.names ./

# Copy the backend application files into the container
COPY backend/ ./backend

# Copy the frontend files into the container
COPY frontend/ ./frontend

# Expose port 8000 for the Flask app
EXPOSE 8000

# Run the Flask app
CMD ["python", "backend/app.py"]
