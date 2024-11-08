// Get button and list elements
const recordButton = document.getElementById('recordButton');
const recordingsList = document.getElementById('recordingsList');

let mediaRecorder;
let audioChunks = [];

// Check if the browser supports getUserMedia
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  console.log("getUserMedia is supported");

  // Set up the button to start recording on mousedown and stop on mouseup
  recordButton.addEventListener('mousedown', async () => {
    // Request access to the microphone
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    // Start recording
    mediaRecorder.start();
    audioChunks = []; // Clear previous audio chunks

    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data); // Collect audio data chunks
    };
  });

  recordButton.addEventListener('mouseup', () => {
    // Stop recording
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
    }

    mediaRecorder.onstop = () => {
      // Create a blob with the recorded audio
      const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
      const audioUrl = URL.createObjectURL(audioBlob);

      // Create audio element and download link
      const audio = document.createElement('audio');
      audio.controls = true;
      audio.src = audioUrl;

      const downloadLink = document.createElement('a');
      downloadLink.href = audioUrl;
      downloadLink.download = 'recording.mp3';
      downloadLink.innerText = 'Download';

      // Append to the list
      const listItem = document.createElement('li');
      listItem.appendChild(audio);
      listItem.appendChild(downloadLink);
      recordingsList.appendChild(listItem);
    };
  });
} else {
  alert("getUserMedia is not supported in this browser.");
}
