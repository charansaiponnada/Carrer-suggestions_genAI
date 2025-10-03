import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from firebase_admin import auth, firestore
from firebase_admin_setup import initialize_firebase, get_db
from ai_engine import initialize_vertex_ai, generate_career_advice # <-- NEW IMPORT
import json # <-- NEW IMPORT for parsing the AI's response

app = FastAPI()

class UserRegistration(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class QuizAnswers(BaseModel):
    uid: str 
    problem_solving_style: str
    team_role: str
    primary_interest: str
    learning_style: str

@app.on_event("startup")
async def startup_event():
    initialize_firebase()
    initialize_vertex_ai()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Career Advisor AI Backend! Firebase is connected."}

@app.post("/register", status_code=201)
async def register_user(user_data: UserRegistration):
    db = get_db()
    try:
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password
        )
        user_profile_data = {
            "uid": user_record.uid,
            "email": user_data.email,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        users_collection = db.collection('users')
        users_collection.document(user_record.uid).set(user_profile_data)
        return {"message": f"User {user_record.email} registered successfully."}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {e}"
        )

@app.post("/login")
async def login_user(user_data: UserLogin):
    try:
        # Read the API key securely from the environment
        api_key = os.getenv("FIREBASE_WEB_API_KEY")
        if not api_key:
            raise ValueError("FIREBASE_WEB_API_KEY is not set in the .env file")

        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        
        payload = {
            "email": user_data.email,
            "password": user_data.password,
            "returnSecureToken": True
        }
        
        response = requests.post(rest_api_url, json=payload)
        response.raise_for_status() # This will raise an error for 4xx or 5xx responses

        data = response.json()
        
        # Important: The UID is called 'localId' in the REST API response
        return {
            "message": "Login successful",
            "uid": data["localId"], 
            "idToken": data["idToken"] # This token can be used for authenticated requests
        }

    except requests.exceptions.HTTPError as err:
        # The API returned an error (like 401, 400, etc.)
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/submit-quiz")
async def submit_quiz(answers: QuizAnswers):
    try:
        db = get_db()
        user_doc_ref = db.collection('users').document(answers.uid)
        quiz_data = {
            "problem_solving_style": answers.problem_solving_style,
            "team_role": answers.team_role,
            "primary_interest": answers.primary_interest,
            "learning_style": answers.learning_style
        }
        user_doc_ref.set({"quiz_results": quiz_data}, merge=True)
        return {"message": f"Quiz results for user {answers.uid} saved successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {e}"
        )

@app.post("/get-recommendation")
async def get_recommendation(data: dict):
    uid = data.get("uid")
    if not uid:
        raise HTTPException(status_code=400, detail="UID is required.")
    try:
        db = get_db()
        user_doc_ref = db.collection('users').document(uid)
        user_doc = user_doc_ref.get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found.")
        user_data = user_doc.to_dict()
        quiz_results = user_data.get("quiz_results")
        if not quiz_results:
            raise HTTPException(status_code=400, detail="User has not completed the quiz yet.")
        ai_response_text = generate_career_advice(quiz_results)
        try:
            clean_response = ai_response_text.strip().replace("```json", "").replace("```", "")
            ai_response_json = json.loads(clean_response)
            return ai_response_json
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Failed to parse AI response. Raw response: {ai_response_text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
