// model.js

document.getElementById('photoInput').addEventListener('change', function(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const preview = document.getElementById('photoPreview');
        preview.src = reader.result;
        preview.style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
});

document.getElementById('captureButton').addEventListener('click', function() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('webcamCanvas');
    const context = canvas.getContext('2d');

    // Set canvas dimensions to match the video feed
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current video frame onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to a data URL and display it as the preview
    const dataURL = canvas.toDataURL('image/png');
    document.getElementById('photoPreview').src = dataURL;
    document.getElementById('photoPreview').style.display = 'block';

    // Clear the file input field since the webcam image is being used
    document.getElementById('photoInput').value = '';
});

document.getElementById('photoForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission behavior
    const formData = new FormData(this);  // Create a FormData object from the form
    const canvas = document.getElementById('webcamCanvas');
    const photoInput = document.getElementById('photoInput');

    // Add the number of recommendations to the form data
    formData.append('num_recommendations', 3);  // Adjust this value as needed

    // If no file is selected and the webcam was used, append the webcam image data to the form
    if (!photoInput.value && canvas.toDataURL('image/png').startsWith('data:image/png')) {
        formData.append('webcam_image', canvas.toDataURL('image/png'));
    }

    // Send the form data to the server via a POST request
    fetch('/capture-photo', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        if (data.success) {
            // Display the detected face shape
            document.getElementById('faceShape').innerText = `Detected Face Shape: ${data.face_shape}`;

            // Display the recommended hairstyles
            const hairstylesDiv = document.getElementById('hairstyles');
            hairstylesDiv.innerHTML = '';  // Clear previous results

            data.hairstyles.forEach(style => {
                const img = document.createElement('img');
                img.src = style;  // Assuming the server returns the image URLs
                img.alt = 'Hairstyle';
                img.className = 'hairstyle-img';

                // Redirect to a specific hairstyle page when the image is clicked
                img.onclick = function() {
                    window.location.href = `/hairstyle/${style.split('/').pop()}`;
                };

                hairstylesDiv.appendChild(img);  // Add the image to the page
            });

            // Show the results section
            document.getElementById('results').style.display = 'block';
        } else {
            // Display an error message if the server returns an error
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);  // Log any errors to the console
    });
});

function startWebcam() {
    const video = document.getElementById('webcam');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;  // Attach the video stream to the video element
                video.play();  // Start playing the video
            })
            .catch(function(error) {
                console.error('Error accessing webcam:', error);  // Log any webcam errors
            });
    } else {
        alert('Webcam not supported by your browser.');
    }
}

// Start the webcam when the page loads
startWebcam();
