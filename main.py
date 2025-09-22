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
# ... (UserRegistration class is here) ...

class QuizAnswers(BaseModel):
    # We will use the user's unique ID to know whose profile to update.
    # The Flutter app will need to send this after the user logs in.
    uid: str 
    problem_solving_style: str
    team_role: str
    primary_interest: str
    learning_style: str

@app.on_event("startup")
async def startup_event():
    initialize_firebase()
    initialize_vertex_ai() # <-- ADD THIS LINE

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Career Advisor AI Backend! Firebase is connected."}

@app.post("/register", status_code=201)
async def register_user(user_data: UserRegistration):
    """
    Endpoint to register a new user.
    - Creates a user in Firebase Authentication.
    - Creates a corresponding user profile in Firestore.
    """
    db = get_db()  # Get the Firestore client

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
# ... (register_user endpoint is here) ...

@app.post("/submit-quiz")
async def submit_quiz(answers: QuizAnswers):
    """
    Endpoint to submit quiz answers for a user.
    Updates the user's profile in Firestore with their answers.
    """
    try:
        # Get the database client
        db = get_db()
        
        # Reference the specific user's document in the 'users' collection
        # The document ID is the user's UID
        user_doc_ref = db.collection('users').document(answers.uid)

        # Prepare the data to be saved. We'll store the answers in a 'quiz_results' map.
        quiz_data = {
            "problem_solving_style": answers.problem_solving_style,
            "team_role": answers.team_role,
            "primary_interest": answers.primary_interest,
            "learning_style": answers.learning_style
        }

        # Update the user's document with the new quiz data.
        # 'set' with 'merge=True' is smart: it adds or updates fields
        # without deleting existing data like 'email' or 'created_at'.
        user_doc_ref.set({"quiz_results": quiz_data}, merge=True)

        return {"message": f"Quiz results for user {answers.uid} saved successfully."}

    except Exception as e:
        # A general catch-all for errors, like if the UID doesn't exist.
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {e}"
        )

@app.post("/get-recommendation")
async def get_recommendation(data: dict):
    """
    Takes a user's UID, fetches their quiz data, and returns AI-generated career advice.
    """
    uid = data.get("uid")
    if not uid:
        raise HTTPException(status_code=400, detail="UID is required.")

    try:
        db = get_db()
        # Fetch the user's document from Firestore
        user_doc_ref = db.collection('users').document(uid)
        user_doc = user_doc_ref.get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Extract the quiz results from the document
        user_data = user_doc.to_dict()
        quiz_results = user_data.get("quiz_results")

        if not quiz_results:
            raise HTTPException(status_code=400, detail="User has not completed the quiz yet.")
        
        # Call our AI engine function with the quiz results
        ai_response_text = generate_career_advice(quiz_results)

        # The AI should return a JSON string. We need to parse it into a real JSON object.
        # NEW AND IMPROVED CODE
        try:
            # Clean the string: remove markdown and leading/trailing whitespace
            clean_response = ai_response_text.strip().replace("```json", "").replace("```", "")
            
            # Now, parse the clean string
            ai_response_json = json.loads(clean_response)
            return ai_response_json
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Failed to parse AI response. Raw response: {ai_response_text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")