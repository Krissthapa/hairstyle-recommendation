import os
from flask import Flask, render_template, request, url_for
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
# Import your custom modules
# from face_detection import detect_face_landmarks
# from face_classification import classify_face_shape
# from hairstyle_recommendation import recommend_styles

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture-photo', methods=['POST'])
def capture_photo():
    try:
        # Check if the request contains a file
        if 'photo' in request.files:
            photo = request.files['photo'].read()  # Read the file as bytes
            image = Image.open(BytesIO(photo))  # Open the image using PIL
        else:
            return 'No photo uploaded. Please try again.', 400

        # Convert the PIL image to a NumPy array
        image_np = np.array(image)

        # Ensure the image is in BGR format for OpenCV
        if image_np.ndim == 2:  # Grayscale image
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        elif image_np.shape[2] == 4:  # RGBA image
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
        elif image_np.shape[2] == 3:  # Already in RGB, convert to BGR
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Example: Process the image (pseudo-code)
        # landmarks = detect_face_landmarks(image_np)
        # face_shape = classify_face_shape(landmarks)
        
        # For the example, let's assume a placeholder response
        face_shape = "Oval"
        hairstyles = ["Style1", "Style2", "Style3"]
        beards = ["Beard1", "Beard2", "Beard3"]

        # Render the template with the recommendations
        return render_template('index.html', hairstyles=hairstyles, beards=beards, face_shape=face_shape)

    except Exception as e:
        import traceback
        print(f"Error in capture_photo: {traceback.format_exc()}")
        return 'An error occurred. Please try again.', 500

if __name__ == '__main__':
    app.run(debug=True)
