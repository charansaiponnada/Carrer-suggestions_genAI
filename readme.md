
# Personalized Career and Skills Advisor

**A Generative AI-powered career mentor built for the Google Cloud Gen AI Exchange Hackathon.**

This project is the backend service for a personalized AI career advisor designed to guide Indian students through the complexities of career choices. It moves beyond generic advice by creating a unique "Career Fingerprint" for each user based on their aptitude, personality, and interests. Using Google Cloud's Vertex AI with Gemini, it recommends tailored career paths, identifies skill gaps, and generates actionable learning roadmaps to prepare students for the evolving job market.

## ✨ Core Features

- **👤 Career Fingerprint Quiz:** Captures a user's unique profile through a simple quiz.
- **🧠 AI-Powered Recommendations:** Leverages a Large Language Model (Gemini on Vertex AI) to provide personalized career suggestions.
- **🗺️ Dynamic Learning Roadmaps:** Generates actionable first steps for learning, tailored to the user's preferred style.
- **GAP Analysis:** Identifies essential skills required for recommended careers.
- **🔐 Secure User Management:** Uses Firebase for robust user authentication and profile storage.
- **🚀 Scalable Architecture:** Built with FastAPI, ready for high-performance, asynchronous workloads.

## 🏗️ System Architecture

The application is built on a modern, decoupled architecture:

- **Frontend (Conceptual):** A Flutter application (for both mobile and web) that provides the user interface.
- **Backend:** A Python-based API built with **FastAPI** that serves as the brain of the operation.
- **Authentication & Database:** **Firebase Authentication** for user management and **Firestore** for storing user profiles and quiz results.
- **AI Engine:** **Google Cloud Vertex AI**, which hosts the **Gemini** generative model to provide intelligent career advice.

```mermaid
graph TD
    A[Flutter App] --> B[FastAPI Backend];
    B --> C[Firebase Auth];
    B --> D[Firestore Database];
    B --> E[Google Cloud Vertex AI];
````

## 🛠️ Tech Stack

* **Backend:** Python 3.9+, FastAPI, Uvicorn
* **AI / ML:** Google Cloud Vertex AI (Gemini Pro model)
* **Database:** Google Firestore
* **Authentication:** Firebase Authentication
* **Infrastructure:** Google Cloud Platform (GCP)
* **Dev Tools:** Git, VS Code, GCloud CLI

## 🚀 Getting Started

Follow these instructions to get the backend server running on your local machine.

### Prerequisites

* Python 3.9+
* Google Cloud SDK (gcloud CLI)
* A Google Cloud / Firebase Project

### 1. Cloud & Firebase Setup (The Critical Part)

* **Create a Firebase Project:** Go to the Firebase Console and create a new project. This automatically creates a linked Google Cloud project. Note your Project ID.
* **Enable Firestore and Authentication:**

  * In Firebase, enable Firestore Database (start in test mode for development).
  * Enable Authentication and add the "Email/Password" sign-in provider.
* **Enable GCP APIs:** In the Google Cloud Console, ensure the correct project is selected and enable the following APIs:

  * Vertex AI API
  * Compute Engine API (This is a crucial prerequisite for Vertex AI in new projects).
* **Enable Billing:** You must enable billing on your Google Cloud project. Vertex AI requires this, but you will stay within the generous free tier for this hackathon.
* **Configure IAM Permissions (The Final Boss):**

  * Go to IAM & Admin > IAM in the Google Cloud Console.
  * Find the Service Account principal (its email ends in @...iam.gserviceaccount.com).
  * Click the pencil icon to edit its roles.
  * Grant it the "Vertex AI Administrator" role. This is the permission your code needs to call the AI model.

### 2. Local Backend Setup

* **Clone the repository:**

```bash
git clone <your-repo-url>
cd career_advisor_backend
```

* **Create and activate a virtual environment:**

```bash
# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.venv\Scripts\activate
```

* **Install dependencies:**

```bash
pip install -r requirements.txt
```

* **Configure Secret Files:**

  * **Firebase Credentials:** In your Firebase project settings, go to "Service accounts" and generate a new private key. This will download a JSON file. Move this file into your project folder and rename it to `firebase_credentials.json`.
  * **Environment Variables:** Create a file named `.env` in the root of the project folder and add the following, replacing with your actual Project ID:

  ```env
  GOOGLE_APPLICATION_CREDENTIALS="firebase_credentials.json"
  GCLOUD_PROJECT="your-gcp-project-id-here"
  ```

* **Git Ignore:** Create a `.gitignore` file and add the following lines to ensure you never commit your secrets:

  ```gitignore
  .venv
  __pycache__/
  .env
  firebase_credentials.json
  ```

* **Authenticate gcloud CLI:**

```bash
gcloud init
gcloud auth application-default login
```

### 3. Running the Server

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

The server will be running at `http://127.0.0.1:8000`.

## 📖 API Endpoints

Navigate to `http://127.0.0.1:8000/docs` for a live, interactive API documentation (Swagger UI).

| Method | Endpoint              | Description                                         | Request Body Example                                                                                                                                   |
| ------ | --------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| POST   | `/register`           | Registers a new user.                               | `{"email": "user@example.com", "password": "password123"}`                                                                                             |
| POST   | `/submit-quiz`        | Submits career fingerprint quiz answers for a user. | `{"uid": "...", "problem_solving_style": "Logical puzzles", "team_role": "The planner", "primary_interest": "Technology", "learning_style": "Videos"}` |
| POST   | `/get-recommendation` | Fetches AI-powered career advice for a user.        | `{"uid": "user_firebase_uid_here"}`                                                                                                                    |

## 🔮 Future Work

* **Frontend Development:** Build the Flutter mobile and web application.
* **Real-Time Market Data:** Integrate live job APIs (e.g., LinkedIn, Naukri) to align recommendations with current market trends.
* **Expanded Quiz:** Enhance the career fingerprint quiz with more psychometric and aptitude questions.
* **Continuous Feedback Loop:** Allow users to rate recommendations to fine-tune the AI model over time.

