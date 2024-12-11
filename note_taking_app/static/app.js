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
