# 🧑‍💻 Data Analyst Agent

The **Data Analyst Agent** is an AI-powered system that turns natural language questions into executable data analysis workflows.

### 🔹 What it does

* Accepts a **question file** (`questions.txt`) plus optional supporting files (CSV, Excel, images, etc.).
* Uses **Google Gemini** to break down the question into smaller, executable steps.
* Generates and runs **Python code** for data processing, analysis, or web scraping.
* Produces final answers in the **format requested by the question**, including numbers, text, or base64-encoded plots.
* Handles errors gracefully by retrying or returning **dummy fallback guesses** only for failed steps.

### 🔹 Key Features

* Multi-file input support (always `questions.txt`, others optional).
* Strict use of uploaded files & real column names — avoids “hallucinated” inputs.
* JSON-safe outputs (auto converts numpy types, base64 encodes images).
* Clear separation between intermediate steps and final user answers.

### 🔹 Usage

Run the code in python using uvicorn app.main:app --reload
Send a POST request to /api/ with questions.txt (required) and any supporting files (optional). For example, in bash run the command curl "https://app.example.com/api/" -F "questions.txt=@question.txt" -F "image.png=@image.png" -F "data.csv=@data.csv"
The folders network, sales and weather contain sample test cases that can be used to test the working of the project. 