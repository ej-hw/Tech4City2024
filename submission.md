# Sentiment Analysis Web Application

## Objective
Build an AI web application for Sentiment Analysis.

## Technologies Used
- HTML
- CSS
- Python
- Vanilla JavaScript
- Flask
- Docker

## Repository Structure


# Instructions
## Prerequisites
- Docker installed on your machine
## Steps to Build and Run the Application
- Clone the repository:
- Build the Docker image:
    ```
    docker build -t sentiment-analysis-app .
    ```
- Run the Docker container:
    ``` 
    docker run -p 5000:5000 sentiment-analysis-app
    ```
- Access the application in your browser:
    Navigate to http://localhost:5000




# Additional Information
- The application uses NLTK for text processing and Scikit-Learn for machine learning.
- The model is trained on 50,000 IMDB movie reviews.