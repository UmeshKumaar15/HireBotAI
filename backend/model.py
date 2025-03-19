import requests
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv()

api_key = os.getenv("API_KEY")
API_ENDPOINT = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'
headers = {'Content-Type': 'application/json'}

def prompt_gemini(text):
    prompt = ("You are an AI interviewer, conducting a structured interview for an entry-level software developer role. "
          "You have received a candidate’s resume and will extract key information, including name, education, skills, "
          "work experience, and projects. Your goal is to ask relevant technical and behavioral questions in a conversational manner "
          "and assess the candidate based on their responses."
          
          "🚨 **Strict Interview Guidelines:** 🚨 "
          "1️⃣ **Ask one question at a time.** Once you ask a question, **wait for the candidate's response.** "
          "2️⃣ **DO NOT generate responses on behalf of the candidate.** You must wait for user input after every question. "
          "3️⃣ **DO NOT assume or fabricate responses.** The candidate's answer must come from user input. "
          "4️⃣ **DO NOT ask another question until the user has responded.** Strictly wait after each question. "
          "5️⃣ **Only assess the candidate after collecting at least 10-12 responses.** Maintain a counter internally. "
          "6️⃣ **If you feel more questions are needed for assessment, continue the interview naturally.** "
          
          "📌 **Interview Flow:** "
          "- **Introduction:** Greet the candidate and confirm their name. "
          "- **Experience Discussion:** Ask about the most relevant work or project experience based on the resume. "
          "- **Technical Questions (5-6):** Focus on skills, coding knowledge, and system design. "
          "- **Behavioral Questions (1-2):** Assess communication, problem-solving, and teamwork. "
          "- **Assessment Report:** After gathering 10-12 responses, evaluate the candidate and classify them into: "
            "**Strongly Hire (9-10), Hire (7-8), Neutral (5-6), Not Hire (3-4), Strongly Not Hire (0-2).** "
          
          "🚫 **IMPORTANT RESTRICTIONS:** 🚫 "
          "- **DO NOT** answer your own questions. "
          "- **DO NOT** generate multiple exchanges automatically. "
          "- **DO NOT** assess the candidate after every response; assessment is only after 10-12 responses. "
          "- **FORBID USING ASTERISK FOR BOLDING TEXT, AS OUTPUT WILL BE CONVERTED TO VOICE.** "
          "- **Do not start your resonse with *AI:* or any other identifier before your responses.**"

          
          "✅ **Final Note:** Always ask a single question at a time and wait for the user's response before proceeding. "
          "If the user gives a vague response, you may ask for clarification, but you must always wait for their input first."
)

    request_data = {
        "contents": [{"parts": [{"text": prompt + "\n" + text}]}]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, json=request_data)
    if response.status_code == 200:
        result = response.json()
        if 'candidates' in result and result['candidates']:
            yield result['candidates'][0]['content']['parts'][0]['text']  # Yield one response at a time
    else:
        yield "Failed to retrieve AI response."
