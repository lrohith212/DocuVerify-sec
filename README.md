# DocuVerify — AI-Powered Document Forensic & Threat Analysis Platform

> **Hackathon Finalist Submission** > An automated, multi-layered digital forensic engine designed to detect document manipulation, AI-generated alterations, mathematical invoice inconsistencies, and embedded PDF threats.


## Overview & Forensic Visuals

| ELA Forensic Heatmap | AI Noise Variance Analysis | Semantic Audit Dashboard |



## The Problem

With the rise of generative AI (e.g., Photoshop Generative Fill, Midjourney, LLMs), manipulating official documents, fake degree certificates, bank statements, and invoices has become effortlessly convincing to the human eye. Manual verification is slow, unreliable, and fails to catch microscopic digital tampering.

## The Solution

**DocuVerify** acts as a automated, zero-trust document security pipeline. Instead of evaluating documents visually, it converts documents into mathematical matrices to catch edits at the pixel, structural, and semantic levels.


## Core Forensic Pipeline & Algorithms
---



## 🛠️ Tech Stack



* **Backend Framework:** Python (Flask), Flask-CORS

* **Computer Vision & Matrix Operations:** OpenCV, NumPy, Pillow (PIL)

* **Document Parsing & Cyber Security:** PyMuPDF (`fitz`), PyPDF2

* **Optical Character Recognition (OCR):** Tesseract OCR via `pytesseract`

* **Frontend:** HTML5, Modern CSS3 (CSS Grid/Flexbox), JavaScript (Fetch API)



---



## ⚡ Quick Start & Installation



### Prerequisites

* Python 3.9+ installed

* Tesseract OCR installed on your host system



### 1. Clone the Repository

```bash

git clone [https://github.com/your-username/DocuVerify.git](https://github.com/your-username/DocuVerify.git)

cd DocuVerify

2. Setup Backend

Bash



cd backend

python -m venv venv# On Windows:

venv\Scripts\activate# On Mac/Linux:source venv/bin/activate



pip install -r requirements.txt

3. Run the Server

Bash



python app.py

The server will start at http://localhost:5000.



4. Run the Frontend

Open frontend/index.html in your web browser or launch it using VS Code Live Server.



## 4. Git Commands to Push to GitHub



Run these commands in your terminal to initialize and push your repository cleanly:



```bash

# 1. Initialize git (if not already initialized)

git init



# 2. Add all files

git add .



# 3. Commit your clean project

git commit -m "Feat: Final hackathon submission - Complete DocuVerify Forensic Platform"



# 4. Set main branch and link your remote repository

git branch -M main

git remote add origin https://github.com/YOUR_GITHUB_USERNAME/DocuVerify.git



# 5. Push code to GitHub

git push -u origin main --force
