Sentiment Fullstack Project
Prepared by: Anwar Ali
Program: Applied AI Solutions Development
Institution: George Brown College
Date: December 2025
Overview
This project is a fullstack system that collects, processes, and analyzes written comments from different online sources. The goal is to help users understand how people feel about a product or topic based on the text they share. The system includes a backend for data collection and sentiment analysis, and a Streamlit dashboard for visualization.
The work reflects principles taught in the Full Stack Data Science Systems course, including design of APIs, model integration, data workflows, error handling, and interface development.
Project Objectives
Collect written comments from online platforms
Process and clean the text before analysis
Apply a sentiment model to classify each comment
Present clear results through an interactive dashboard
Demonstrate fullstack data flow from input to final output
System Structure
The project has two main components:
Backend
The backend provides the API routes that handle requests from the dashboard.
Key functions include:
Processing plain text inputs
Collecting YouTube comments using the YouTube API
Using a local fallback dataset to demonstrate Amazon review analysis
Running sentiment predictions
Returning structured results to the frontend
The backend is built with FastAPI and organized into modular files (main, youtube_client, amazon_client, model_loader, schemas).
Frontend
The dashboard is built with Streamlit.
Its purpose is to provide a simple interface where users can:
Analyze a single text input
Analyze YouTube comments from any public video
Analyze sample Amazon product reviews (local dataset)
View sentiment distribution charts and sample outputs
Sentiment Model
The system uses a loaded sentiment model that assigns each text a label (positive or negative) and a score.
The model is integrated through a dedicated file, allowing the backend to call it for each comment.
Features Demonstrated
Clean separation of backend and frontend
API design and error handling
Use of external APIs
Data processing and response modeling
Deployment-ready project structure
Interactive dashboard for presentation

