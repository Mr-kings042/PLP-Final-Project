from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from utils.db import  get_notes, add_note_to_db, delete_note_from_db, edit_note_in_db, update_note_in_db
from utils.file_utils import generate_txt, generate_docx
from utils.pdf_utils import generate_pdf
import speech_recognition as sr

import os
import tempfile



# Flask App
app = Flask(__name__)


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

@app.route("/edit/<int:note_id>", methods=["POST"])
def edit_note(note_id):
    """Edit a saved note."""
    data = request.json
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    if title and content:
        edit_note_in_db(note_id, title, content)
        return jsonify({"message": "Note updated successfully!"}), 200
    return jsonify({"message": "Invalid data."}), 400

@app.route("/download/<int:note_id>/<format>")
def download_note(note_id, format):
    """Download a note in the specified format."""
    note = next((n for n in get_notes() if n[0] == note_id), None)
    if not note:
        return "Note not found", 404

    title, content = note[1], note[2]
    if format == "txt":
        file_path = generate_txt(title, content)
    elif format == "pdf":
        file_path = generate_pdf(title, content)
    elif format == "docx":
        file_path = generate_docx(title, content)
    else:
        return "Invalid format", 400

    return send_file(file_path, as_attachment=True)
@app.route('/update-note', methods=['POST'])
def update_note():
    data = request.json
    print(f"Received data: {data}")
    note_id = data.get('id')  # Ensure the ID is passed in the request
    title = data.get('title')
    content = data.get('content')

    if not all([note_id, title, content]):
        return jsonify({'error': 'Invalid data provided'}), 400

    success = update_note_in_db(note_id, title, content)
    if success:
        print("Note updated successfully")
        print(f"Updated notes: {get_notes()}") 
        return jsonify({'message': 'Note updated successfully'}), 200
    else:
        print("Failed to update note")
        return jsonify({'error': 'Failed to update the note'}), 500
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
    app.run(host='127.0.0.1', port=5000,debug=True)
