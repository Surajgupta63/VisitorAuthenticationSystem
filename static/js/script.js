let video = document.getElementById("video");
let captureButton = document.getElementById("captureButton");
let takePhotoButton = document.getElementById("takePhotoButton");
let retakeButton = document.getElementById("retakeButton");
let uploadButton = document.getElementById("uploadBtn");
let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let mediaStream = null;
let capturedImageDiv = document.getElementById("capturedImageDiv");
let capturedImage = document.getElementById("capturedImage");

// Start webcam on button click
function startCamera() {
    captureButton.disabled = true;
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            mediaStream = stream;
            takePhotoButton.disabled = false;
            retakeButton.disabled = true;
        })
        .catch((err) => { 
            console.error("Error accessing webcam: ", err);
            alert("Error accessing the webcam.");
        });
}

// Capture photo when button is clicked
function capturePhoto() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Stop the camera after capture
    mediaStream.getTracks().forEach(track => track.stop());

    // Resize the image before uploading
    resizeImage(canvas.toDataURL("image/png")).then((resizedDataUrl) => {
        capturedImage.src = resizedDataUrl;
        capturedImageDiv.style.display = 'block';

        // Enable upload and retake buttons
        uploadButton.disabled = false;
        retakeButton.disabled = false;
        takePhotoButton.disabled = true;

        // Set image data in hidden form field
        document.getElementById("imageData").value = resizedDataUrl;
    });
}

// Retake photo: Restart the camera and hide the previous image
function retakePhoto() {
    capturedImageDiv.style.display = "none";
    uploadButton.disabled = true;
    takePhotoButton.disabled = false;
    retakeButton.disabled = true;
    startCamera(); // Restart the camera
}

// Resize image function (limits the size to 1MB)
function resizeImage(dataUrl) {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => {
            const MAX_WIDTH = 640;
            const MAX_HEIGHT = 480;

            let width = img.width;
            let height = img.height;

            // Calculate new dimensions while maintaining aspect ratio
            if (width > height) {
                if (width > MAX_WIDTH) {
                    height = Math.round(height * MAX_WIDTH / width);
                    width = MAX_WIDTH;
                }
            } else {
                if (height > MAX_HEIGHT) {
                    width = Math.round(width * MAX_HEIGHT / height);
                    height = MAX_HEIGHT;
                }
            }

            // Create a new canvas to resize the image
            const canvasResized = document.createElement("canvas");
            const ctxResized = canvasResized.getContext("2d");
            canvasResized.width = width;
            canvasResized.height = height;
            ctxResized.drawImage(img, 0, 0, width, height);

            // Return the resized image as a DataURL
            resolve(canvasResized.toDataURL("image/png"));
        };
        img.src = dataUrl;
    });
}
