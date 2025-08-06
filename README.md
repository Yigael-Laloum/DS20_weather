# DS20_weather
# Weather Data Fetching Application

My DS20 first project

Project Overview
This is the first project for the DS20 course, focused on building an interactive Python application to fetch and display weather data for any specified location. The application is built using Streamlit to provide a user-friendly web interface and leverages a RESTful API from a weather data provider to retrieve accurate, real-time information.

This project is a great opportunity to strengthen my understanding of Python programming, working with JSON structures, and integrating with external APIs. Furthermore, the use of Poetry for dependency management ensures a clean and reproducible development environment.

Key Features and Functionalities
Real-time Weather Data: Users can enter any city name to get current weather conditions, including:

Current temperature in Celsius (°C).

Humidity percentage.

A descriptive text and icon of the current weather condition (e.g., "partly cloudy").

Interactive Visualizations: The application uses Plotly to create engaging visual representations of the data:

An interactive gauge chart that dynamically displays the current temperature.

A second gauge chart showing the current humidity level.

These charts provide an instant, intuitive understanding of the weather conditions.

5-Day Forecast: The application fetches and displays a detailed forecast for the next five days, presented in an easy-to-read, column-based layout. This includes:

Daily minimum and maximum temperatures.

A weather description and corresponding icon for each day.

Robust Error Handling: The application gracefully handles various potential issues, such as:

Invalid or non-existent city names.

Connection failures to the API.

Technologies Used
Python: The core programming language for the entire application logic.

Streamlit: The framework used to create the interactive web application and its user interface.

Requests: A Python library for making HTTP requests to the weather API.

Plotly: Used for generating dynamic and interactive charts to visualize the data.

Poetry: Employed for efficient and reliable management of project dependencies and virtual environments.

Getting Started
To run this project locally, follow these steps:

Clone the repository:
git clone [your-repo-url]

Install dependencies:
poetry install

Run the Streamlit application:
streamlit run your_app_file_name.py

