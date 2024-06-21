# Real Estate Project Analysis App

This Streamlit application allows users to analyze a real estate project and compare it with nearby competitive projects. It provides detailed information about air quality and nearby facilities.

## Features

- Retrieve and display the coordinates of a specified real estate project.
- Identify and display competitive real estate projects in the vicinity.
- Retrieve and display air quality data for the specified project and its competitors.
- Retrieve and display nearby facilities (e.g., schools, hospitals, restaurants) for each project.
- Generate a comprehensive analysis report comparing the main project with its competitors.

## Setup

1. Create a virtual environment and install dependencies:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

2. Set up API keys:
    - Obtain API keys for Foursquare, OpenWeatherMap, and Groq.
    - Create a `.env` file in the root directory and add the following lines, replacing the placeholders with your actual API keys:
      ```
      FOURSQUARE_API_KEY=your_foursquare_api_key
      OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
      GROQ_API_KEY=your_groq_api_key
      ```

3. Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Enter the name of the main real estate project in the input field.
2. Click the "Analyze" button to start the analysis.
3. The app will display:
    - Coordinates of the main project.
    - Competitive real estate projects in the vicinity with detailed information.
    - Air quality data for the main project and its competitors.
    - Nearby facilities for each project.
4. A comprehensive analysis report will be generated, comparing the main project with its competitors and providing reasoning and grades for each project.



## Technologies Used

- **Streamlit**: For building the interactive web application.
- **Requests**: For making API calls to Foursquare, OpenWeatherMap, and Groq.
- **Groq**: For generating a detailed comparative analysis report.

## Note of Gratitude

I am grateful for the opportunity to work on this assignment. Thank you for giving me this assignment; I learned a lot from this project.
