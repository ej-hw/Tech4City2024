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
    docker build -t application .
    ```
- Run the Docker container:
    ``` 
    docker run -p 8000:8000 application
    ```

- Access the application in your browser:
    Navigate to http://localhost:8000 or http://127.0.0.1:8000/

- The following is what you should see

    ![GUI!](/gui_screenshot.png)

- Train the model (by clicking retrain the model)
    Note, if you do not retrain the model, and click <em>Predict Sentiment </em>, you will see an error. 

    ![terminal screenshot!](/terminal_screenshot.png)

- Make a prediction by keying in a model review after training is complete

- Watch the demo video [here](https://www.youtube.com/watch?v=ks0htbD0fmY)




# Additional Information
- The application uses NLTK for text processing and Scikit-Learn for machine learning.
- The model is trained on 50,000 IMDB movie reviews.
- The model is saved and cached in memory. 