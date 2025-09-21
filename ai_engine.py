import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

def initialize_vertex_ai():
    """Initializes the Vertex AI SDK with the project and location."""
    load_dotenv() # Make sure environment variables are loaded
    PROJECT_ID = os.environ.get('GCLOUD_PROJECT')
    if not PROJECT_ID:
        raise ValueError("GCLOUD_PROJECT environment variable not set. Please check your .env file.")

    # For this hackathon, let's use a region that supports Gemini well, like us-central1
    LOCATION = "us-central1"
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print(f"Vertex AI initialized for project: {PROJECT_ID} in location: {LOCATION}")


def generate_career_advice(quiz_results: dict) -> str:
    """
    Generates career advice using Google's Gemini model based on quiz results.
    """
    
    # Initialize the specific generative model we want to use
    model = GenerativeModel("gemini-pro")

    # --- The Prompt ---
    prompt = f"""
    You are an expert career advisor for students in India. Your goal is to provide personalized, actionable, and encouraging advice.

    A student has just completed a career profiling quiz. Here are their results:
    - They enjoy problem-solving by: {quiz_results.get('problem_solving_style', 'not specified')}
    - In a team, their natural role is: {quiz_results.get('team_role', 'not specified')}
    - Their primary field of interest is: {quiz_results.get('primary_interest', 'not specified')}
    - Their preferred learning style is: {quiz_results.get('learning_style', 'not specified')}

    Based ONLY on this information, perform the following tasks:

    1.  **Recommend 3 specific and suitable career paths.** For each career, provide a one-sentence description of why it fits their profile.
    2.  **Identify the top 3-5 essential skills** required to succeed in these recommended paths.
    3.  **Create a simple, actionable "First Steps" learning roadmap.** This should be a list of 3-4 concrete actions the student can take, tailored to their learning style.

    **IMPORTANT:** Your entire response MUST be in a valid, minified JSON format. Do not include any text before or after the JSON object. The JSON object should have the following structure:
    {{
      "recommended_careers": [
        {{"career": "Career Name 1", "reason": "Reason why it fits."}},
        {{"career": "Career Name 2", "reason": "Reason why it fits."}},
        {{"career": "Career Name 3", "reason": "Reason why it fits."}}
      ],
      "essential_skills": ["Skill 1", "Skill 2", "Skill 3", "Skill 4"],
      "learning_roadmap": [
        "First step tailored to their learning style.",
        "Second step tailored to their learning style.",
        "Third step tailored to their learning style."
      ]
    }}
    """

    response = model.generate_content(prompt)
    return response.text