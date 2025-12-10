# Sentiment Analysis Full-Stack System

This project is a complete sentiment analysis system that collects, processes, and analyzes text from different online sources. It uses a FastAPI backend for handling requests and a Streamlit interface for visualizing the results. The system can classify text as positive, negative, or neutral using several machine learning and deep learning models.

---

## Project Overview

The goal of this project is to help users understand how people feel about a product or topic by analyzing written comments. The system takes text from different platforms, cleans it, runs it through sentiment models, and then shows the results in a simple dashboard. I used FastAPI to build the backend and Streamlit to build the interface. The project includes several models so I could compare how they perform on the same data.

---

## Models Used

To understand the difference between traditional machine learning and deep learning approaches, I trained several models on the same dataset:

• Logistic Regression  
• Feed-Forward Neural Network  
• LSTM  
• DistilBERT  

Each model was evaluated on accuracy, precision, recall, and F1-score. This made it easy to compare their strengths and weaknesses.
 

## System Structure

The system is built in two main parts. The first part is the backend, created with FastAPI. It receives text, cleans it, runs it through the selected model, and returns the sentiment result. The second part is the Streamlit interface. This is where users can enter text, run the analysis, and see the output. The dashboard also displays counts, charts, and sample results.

This setup separates the model logic from the user interface, making the system easier to manage and update.
  

---

## How to Run the System

The project has two parts, the FastAPI backend and the Streamlit dashboard. Each one needs to be started separately.

### 1. Start the FastAPI backend
Open your terminal, go to the project folder, and run:

uvicorn main:app --reload

This starts the API. It will show the URL in the terminal, usually something like:

http://127.0.0.1:8000

Keep this running.

### 2. Start the Streamlit dashboard
Open a new terminal window and run:

streamlit run streamlit_app.py

The dashboard will open in your browser. From there you can enter text, run the analysis, and see the results.


---

## Results

Each model performed differently based on how it handles text. Logistic Regression worked well for simple patterns. The feed-forward network improved on that by learning from more features. The LSTM did better with longer sentences because it can understand sequence information. DistilBERT gave the strongest results overall since it is built on a modern transformer architecture. The dashboard shows the predictions clearly so users can compare the outcomes across different models.

## What I Learned

I learned how to build a full workflow that goes from data collection, to text cleaning, to training several models, and finally to building a usable application. Working with FastAPI and Streamlit helped me understand how machine learning models can be turned into practical tools. Training and comparing different models also gave me a better sense of how text classifiers behave and what affects their performance.

