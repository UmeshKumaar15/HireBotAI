from speech_module.tts import TextToSpeech
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from app_functions import extract_text_from_pdf
from model import prompt_gemini

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Prevent CORS issues

tts = TextToSpeech()  # Global instance to avoid reinitialization issues

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interview', methods=['POST'])
def interview():
    file = request.files.get('file')
    if not file:
        return "No file uploaded", 400

    text_content = extract_text_from_pdf(file)
    session['conversation_history'] = [f"Resume: {text_content}"]
    session['ai_turn'] = True
    session['first_message_sent'] = False  # Ensure AI only speaks once

    return render_template('interview.html')

@socketio.on('connect')
def handle_connect():
    """ Ensures AI only speaks once per user connection. """
    if "first_message_sent" not in session:
        session['first_message_sent'] = False

@socketio.on('start_interview')
def handle_start_interview():
    if session.get('ai_turn', False) and not session.get('first_message_sent', False):
        session['first_message_sent'] = True  # Set flag to prevent repetition

        conversation_history = session.get('conversation_history', [])
        first_ai_message = next(prompt_gemini("\n".join(conversation_history)))
        session['conversation_history'].append(f"AI: {first_ai_message}")
        session['ai_turn'] = False  # AI turn flag reset

        # Speak First AI Response
        tts.speak(first_ai_message)

        socketio.emit('ai_response', {'message': first_ai_message})

@socketio.on('user_response')
def handle_user_response(data):
    user_message = data.get('message')
    if user_message:
        session['conversation_history'].append(f"User: {user_message}")
        session['ai_turn'] = True

        ai_message = next(prompt_gemini("\n".join(session['conversation_history'])))
        session['conversation_history'].append(f"AI: {ai_message}")
        session['ai_turn'] = False  # AI turn flag reset

        # Speak AI Response Every Time
        tts.speak(ai_message)

        socketio.emit('ai_response', {'message': ai_message})
