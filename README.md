# Sentiment Fullstack Project

This project is part of my Applied AI Solutions Development program at George Brown College.  
I wanted to build something practical that collects comments from different online sources, analyzes their sentiment, and shows the results in a simple dashboard.  
The goal is to help a user understand what people are saying about a topic or a product in a clear and organized way.

The system has two parts:

- **Backend (FastAPI)** – handles all processing, API routes, and sentiment predictions  
- **Frontend (Streamlit)** – provides an interface for testing text, YouTube comments, and sample Amazon reviews

---

## 1. Project Overview

The workflow reflects topics from the Full Stack Data Science Systems course, including:

- API design  
- Data collection  
- Data cleaning and preprocessing  
- Model integration  
- Error handling  
- Basic dashboard development  

The system can:

- Collect YouTube comments using the YouTube API  
- Analyze a single text message  
- Process a small sample of Amazon product reviews  
- Apply a sentiment model (positive / negative)  
- Show results in charts and tables inside Streamlit

---

## 2. System Structure

### **Backend (FastAPI)**  
Located in the `backend/` folder.

Main responsibilities:

- Receive text from the dashboard  
- Clean and process the text  
- Run the sentiment model  
- Collect YouTube comments through the API  
- Return structured results to the frontend  

The backend is organized into modular files:

- `main.py` – main application and API routes  
- `youtube_client.py` – collect YouTube comments  
- `amazon_client.py` – local fallback sample dataset  
- `model_loader.py` – load the sentiment model  
- `schemas.py` – request and response models  

### **Frontend (Streamlit)**  
Located in the `frontend/` folder.

Main responsibilities:

- Provide a clean interface  
- Send user inputs to the backend  
- Display results, charts, and tables  
- Make the system easy to test and present  

Users can:

- Analyze a single text  
- Analyze YouTube comments by URL  
- View sentiment breakdowns  
- Explore sample Amazon review analysis  

---

## 3. How to Run the Project

### **1. Start the backend (FastAPI)**

```bash
cd backend
uvicorn main:app --reload
