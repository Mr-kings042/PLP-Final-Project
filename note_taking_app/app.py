from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
import mysql.connector
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables from .env file
load_dotenv()

# Flask App
app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

# Create Notes Table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL
)
""")
db.commit()

# Helper Functions
def get_notes():
    """Fetch all notes from the database."""
    cursor.execute("SELECT id, title, content FROM notes")
    return cursor.fetchall()

def add_note_to_db(title, content):
    """Add a new note to the database."""
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    db.commit()

def delete_note_from_db(note_id):
    """Delete a note from the database."""
    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    db.commit()

# Routes
@app.route ("/")
def index():
    """Home page: display all notes."""
    notes = get_notes()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    """Add a new note."""
    title = request.form["title"].strip()
    content = request.form["content"].strip()
    if title:
        add_note_to_db(title, content)
    return redirect(url_for("index"))

@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    """Delete a note by its ID."""
    delete_note_from_db(note_id)
    return redirect(url_for("index"))

@app.route("/voice", methods=["POST"])
def voice_note():
    """Add a note using voice input."""
    recognizer = sr.Recognizer()
    try:
        # Process voice input
        audio_file = request.files.get("audio")
        if not audio_file:
            print("No audio file received")
            return redirect(url_for("index"))

        # Save audio temporarily for processing
        temp_audio_path = "temp_audio.wav"
        audio_file.save(temp_audio_path)

        # Use SpeechRecognition to process the audio file
        with sr.AudioFile(temp_audio_path) as source:
            audio = recognizer.record(source)
        content = recognizer.recognize_google(audio)

        # Save the note to the database
        if content:
            add_note_to_db("Voice Note", content)
        else:
            print("No content recognized in the audio file")

        # Clean up the temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

    except Exception as e:
        print(f"Error processing voice input: {e}")

    return redirect(url_for("index"))

# Run the App
if __name__ == "__main__":
    app.run(debug=True)
