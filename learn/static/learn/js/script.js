const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const processedImage = document.getElementById('processed-image');
const faceCount = document.getElementById('face-count');

// Initialize WebSocket
const socket = new WebSocket('ws://localhost:8000/ws/process-frame/');

// WebSocket connection events
socket.onopen = () => {
    console.log('WebSocket connection established');
};

socket.onclose = () => {
    console.log('WebSocket connection closed');
};

navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(stream => {
        console.log('Webcam access granted');
        video.srcObject = stream;
        video.play();
    })
    .catch(error => {
        console.error('Error accessing webcam:', error);
        if (error.name === "NotAllowedError") {
            alert("Webcam access was denied. Please allow access to continue.");
        } else {
            alert("Error accessing webcam: " + error.message);
        }
    });

socket.onmessage = event => {
    const data = JSON.parse(event.data);
    if (data.result) {
        // Update the processed image
        processedImage.src = data.result;
        // Update the face count
        faceCount.textContent = `Faces detected: ${data.faces_detected}`;
    } else if (data.error) {
        console.error('Error from backend:', data.error);
    }
};

// Capture and send frames to WebSocket server
// Adjust interval for sending frames to reduce load
setInterval(() => {
    if (!video.srcObject) {
        console.log('Video stream not yet initialized');
        return;
    }

    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current frame onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas frame to Base64
    const frame = canvas.toDataURL('image/jpeg', 0.5); // Reduced quality (0.5) for lower data size
    console.log('Sending frame:', frame.slice(0, 100)); // Log the first 100 characters of the frame
    socket.send(JSON.stringify({ frame: frame }));
}, 1000); // Send a frame every 1 second instead of 500ms
