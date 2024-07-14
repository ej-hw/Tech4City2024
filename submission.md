# MyCoTech-Innovators

## Overview
This project is a FastAPI application that allows users to upload images, classify them, and view the history of uploaded images. 

The application uses a pretrained AI Model, ResNet50 for detection up to 1000 different items, including mushrooms, which we used for our project.

The application uses SQLite for storing image information and predictions.

### Prerequisites
 - Python 3.10
 - Docker (optional, if you want to use Docker for deployment)

 ### Environment Setup
 1. Clone the repository: 
 
    `git clone https://github.com/Mycarhhhhh/MyCoTech-Innovators.git`

 2. `cd project`
 

### Usage
1. **Build and Run the application:**
 type on terminal : `docker build -t mycotech-innovators .`
after that type : `docker run -p 8000:8000 mycotech-innovators`

 2. **Access the application:**
    Open your web browser and go to `http://0.0.0.0:8000`.
    After opening it change the url to `http://127.0.0.1:8000`
    now you can use the application
