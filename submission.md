# Tech4City2024 Entry Coding Challenge Submission

## Team Name
Golden Gamers

## Team Members
- Member 1: Jonathon Leong
- Member 2: Fatin Sharafana
- Member 3: Denise Caluza

## Project Title
Golden Gamers ID Creation App

## Project Description
The Golden Gamers ID Creation App is an AI web application that allows users to create photo IDs for the exergames arcade with position analysis and head detection. Users input data from the local webcam, the AI processes the input to detect the head's position (Centralised, Not Center, or No head detected), and displays the result. Past ID creations are stored in a lightweight local database, stored in the backend and viewable on the frontend.

## Project Features
- **User Interface**: Simple, intuitive, and fun UI for data submission and result display.
- **Position Analysis and Head Detection**: Real-time analysis of user's head position, indicating 'Centralised', 'Not Center', or 'No head detected'.
- **Photo ID Creation**: Users can create a photo ID based on the analysis.
- **Database Storage**: Stores user names and timestamps of each ID creation in database.db.
- **API Documentation**: Documented API endpoints using Swagger.

## How the AI Works
The AI component leverages OpenCV, a powerful computer vision library, for image processing and head detection. Here's a brief overview of how it works:
1. **Webcam Capture**: The application captures real-time video from the user's webcam.
2. **Image Processing**: Each frame of the video is processed using OpenCV to detect the user's head position.
3. **Head Detection**: OpenCV's pre-trained Haar Cascade classifiers are used to identify and locate the user's head in the video frame.
4. **Position Analysis**: The detected head position is analyzed to determine if it is centralized or not, or if no head is detected.
5. **Result Display**: The result of the position analysis is displayed to the user in real-time.

## How to Run the Project
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/jonathon1998/Tech4City2024.git
    cd Tech4City2024
    ```
2. **Set Up the Environment**:
    - Ensure you have Docker installed.
    - Build the Docker image:
      ```bash
      docker build -t position-analysis .
      ```
    - Run the Docker container on port8000:
      ```bash
      docker run -p 8000:8000 position-analysis
      ```
3. **Access the Application**:
    - Open your web browser and navigate to `http://localhost:8000`.

## API Endpoints Documentation
Detailed API documentation can be found in the Swagger UI at `http://localhost:8000/docs`.


## Link to Project Repository
[GitHub Repository](https://github.com/jonathon1998/Tech4City2024)

## Contact Information
- Jonathon Leong: [email to] jonathon@nus.edu.sg

