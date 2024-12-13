let audioRecorder;
let audioBlob;

document.getElementById("startBtn").disabled = false;
document.getElementById("stopBtn").disabled = true;

function startRecording() {
    document.getElementById("status").textContent = "Recording in progress...";
    document.getElementById("startBtn").disabled = true;
    document.getElementById("stopBtn").disabled = false;

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            audioRecorder = new MediaRecorder(stream);

            // Store recorded audio
            audioRecorder.ondataavailable = function (event) {
                audioBlob = event.data;
                const audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById("audio").src = audioUrl;
                document.getElementById("audioPlayer").style.display = 'block';
            };

            audioRecorder.start();
        })
        .catch(err => {
            console.log('Error accessing microphone:', err);
        });
}

function stopRecording() {
    if (!audioRecorder && audioRecorder.state !== "inactive") return;

    audioRecorder.stop();
    document.getElementById("status").textContent = "Recording stopped.";
    document.getElementById("startBtn").disabled = false;
    document.getElementById("stopBtn").disabled = true;

    // Add recording to the notes list
    const newNote = document.createElement("li");
    newNote.textContent = "New Voice Note (Click to play)";
    newNote.addEventListener("click", function () {
        document.getElementById("audio").play();
    });
    document.getElementById("noteList").appendChild(newNote);

    // Upload the audioBlob to the server
    uploadVoiceNote(audioBlob);
}

function uploadVoiceNote(blob) {
    const formData = new FormData();
    formData.append("audio", blob, "voice_note.wav");

    fetch("/voice", {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (response.ok) {
                document.getElementById("status").textContent = "Voice note uploaded successfully!";
            } else {
                document.getElementById("status").textContent = "Failed to upload voice note.";
            }
        })
        .catch(error => {
            console.error("Error uploading voice note:", error);
            document.getElementById("status").textContent = "Error uploading voice note.";
        });
}

document.querySelectorAll('.note').forEach(note => {
    const titleElement = note.querySelector('.note-title');
    const contentElement = note.querySelector('.note-content');
    const editButton = note.querySelector('.edit-btn');
    const saveButton = note.querySelector('.save-btn');

    // Assume each note has a data attribute with its ID
    const noteId = note.dataset.id;

    editButton.addEventListener('click', () => {
        titleElement.setAttribute('contenteditable', 'true');
        contentElement.setAttribute('contenteditable', 'true');
        editButton.style.display = 'none';
        saveButton.style.display = 'inline-block';
        titleElement.classList.add('editable');
        contentElement.classList.add('editable');
    });

    saveButton.addEventListener('click', () => {
        titleElement.setAttribute('contenteditable', 'false');
        contentElement.setAttribute('contenteditable', 'false');
        editButton.style.display = 'inline-block';
        saveButton.style.display = 'none';
        titleElement.classList.remove('editable');
        contentElement.classList.remove('editable');


        const noteId = noteElement.id.replace("note-", "");
        const updatedTitle = titleElement.textContent.trim();
        const updatedContent = contentElement.textContent.trim();

        fetch('/update-note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: noteId,
                title: updatedTitle,
                content: updatedContent,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log(data.message);
            } else {
                console.error(data.error);
            }
        })
        .catch(err => console.error('Error updating note:', err));
    });
});

fetch("/get-notes", {
    method: "GET",
    headers: { "Cache-Control": "no-cache" }
})
.then(response => response.json())
.then(data => {
    console.log(data); // Ensure the most recent notes are fetched
});


// function downloadNote(title, content) {
//     const blob = new Blob([`Title: ${title}\n\n${content}`], { type: "text/plain" });
//     const url = URL.createObjectURL(blob);
//     const a = document.createElement("a");
//     a.href = url;
//     a.download = `${title}.pdf`; // Change to `.pdf`, `.docx`, or `.png` if needed
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//     URL.revokeObjectURL(url);
// }