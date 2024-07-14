Absolutely, here's the edited and formatted text:

**Huawei Tech4City 2024 Competition**

## About

The annual Huawei Tech4City Competition is your chance to embark on a journey towards a more inclusive and sustainable Singapore through technology! This competition equips you with the tools to build and improve your prototypes, turning your creative ideas into reality.

Learn more about the Huawei Tech4City 2024 competition on the official website [**here**](#).

## Entry Challenge

Develop an AI web application that allows users to:

* Input data
* Process the data using AI
* View the results

The application should also store past inputs and results in a local lightweight database for later viewing on the frontend. The application needs to run on an environment with 4vCPU, 16 GB RAM, and no GPU.

**Choose one of the following AI use cases for your application:**

* Sentiment Analysis
* Image Classification
* Object Detection

## Submission Requirements

The challenge focuses on using fundamental knowledge of common coding languages and frameworks. You'll be using HTML, CSS, Python, and vanilla JavaScript.

## Repository Setup

Create a repository with the following structure:

```
frontend/
├── index.html  # Create a form with appropriate input fields (text area for sentiment analysis, file input for image classification or object detection) and a submit button.
├── styles.css  # Style the form and results display area.
└── script.js   # Handle form submission, send input data to the backend API, display the AI result, and fetch/display past inputs and results.

backend/
├── app.py      # Main file for backend code for endpoints:
#                - POST /analyze: Accepts user input, performs AI processing, stores data in the database, and returns the result.
#                - GET /results: Retrieves all stored inputs and their results from the database.
├── model.py    # Implement a function to process the user input using an AI/ML library (e.g., Huggingface, TensorFlow, PyTorch).
└── database.db # Local lightweight database (e.g., sqlite, duckdb)

requirements.txt # File for Python app dependencies
Dockerfile      # Provide a Dockerfile to containerize the application (accessible on port 8000).

submission.md   # Provide your team name and other necessary information for the repository.
```

## Evaluation Criteria

**Frontend**

* User interface design and usability
* Intuitive data submission and result display
* Ability to review historical data submissions and results

**Backend**

* Proper implementation of API endpoints following REST principles
* Effective data storage and retrieval using a local database
* Input validation and error handling
* Database schema design and usage
* API endpoints documentation using OpenAPI (Swagger) or equivalent

**AI Element**

* Use of appropriate techniques for AI processing
* Proper integration between the AI component, backend, and frontend
* Efficiency and effectiveness of the AI model

**Docker**

* Correct setup and configuration of the Dockerfile
* Successful building and running of the Docker container
* Ability to access the application on port 8000 after running the Docker container

**Overall Functionality**

* Completeness of the application and fulfillment of all requirements
* Stability and absence of bugs or crashes
* Innovation and creativity in the implementation
* Code structure and readability

## Submission

Submit your entry (code, datasets, documents) by forking this repository. A submission form will also be available where you can include the link to your fork.

**Steps to Submit**

1. **Create your own fork**

   ```bash
   git clone git@github.com:<your-github-username>/Tech4City2024
   cd Tech4City2024
   git remote add upstream git@github.com:ej-hw/Tech4City2024
   ```

2. **Start hacking!**

3. **Ready to submit?**

   * Create a pull request from your fork to the main repository.
   * Include the link to your fork in the submission form.

**Important Note:**

* Your code will be publicly available, open-sourced, and free to use.
* Please ensure you don't commit any sensitive information!

**Our Team**

* Zhang Haoyu (Hardware Engineer, Undergraduate) - Experience: IoT based weather broadcast clock design
* Wang Boyu (Product Designer, Undergraduate) - Experience: Prototyping and CMF for food waste recycler
* Hu Chong Xern (Software Programmer, Undergraduate) - Experience: Version control and model-view-controller architecture in OISDP (Orbital Independent Software Development Project)
* Sahej Agarwal (Data Scientist, Undergraduate) - Experience: NLP solution development via PyTorch, Algorithms for knee joint MRI segmentation
