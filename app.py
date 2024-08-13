from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import base64
import cv2
import numpy as np
import dlib
import logging
from face_classification import classify_face_shape
from hairstyle_recommendation import recommend_styles

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

# Initialize dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def detect_face_landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        return None, None
    face = faces[0]
    landmarks = predictor(gray, face)
    landmarks_list = [(p.x, p.y) for p in landmarks.parts()]
    return face, landmarks_list
@app.route('/')
def index():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')

    # Log the incoming request data
    logging.debug("Received registration data: %s", request.form)

    # Check if form data is received correctly
    if not username or not email:
        logging.error("Missing username or email in the form data.")
        return jsonify({"error": "Missing username or email"}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        logging.info("User already exists: %s. Allowing access.", username)
        return jsonify({"message": "Welcome back, {}!".format(username)}), 200

    # Create a new user and add to the database
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    logging.info("User registered successfully: %s", username)
    return jsonify({"message": "Registration successful"}), 200


@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/capture-photo', methods=['POST'])
def capture_photo():
    try:
        photo = None
        image = None

        # Check if the file is uploaded via form-data
        if 'photo' in request.files and request.files['photo'].filename != '':
            photo = request.files['photo'].read()
            image = Image.open(BytesIO(photo))
            logging.debug("Photo uploaded via form-data.")
        # Check if the image is sent via base64 encoded string
        elif 'webcam_image' in request.form:
            photo_data = request.form['webcam_image'].split(',')[1]
            photo = base64.b64decode(photo_data)
            image = Image.open(BytesIO(photo))
            logging.debug("Photo uploaded via base64 encoded string.")
        else:
            logging.error("No valid image provided.")
            return jsonify({'success': False, 'error': 'No valid image provided.'}), 400

        # Ensure num_recommendations is an integer
        try:
            num_recommendations = int(request.form.get('num_recommendations', 3))
        except ValueError:
            logging.error("Invalid value for num_recommendations.")
            return jsonify({'success': False, 'error': 'Invalid value for num_recommendations.'}), 400

        # Convert PIL image to NumPy array
        image_np = np.array(image)

        if image_np.ndim == 2:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        elif image_np.shape[2] == 4:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
        elif image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        face, landmarks = detect_face_landmarks(image_np)
        if landmarks is None:
            logging.error("No face detected in the image.")
            return jsonify({'success': False, 'error': 'No face detected.'}), 400

        face_shape = classify_face_shape(landmarks)
        hairstyles = recommend_styles(face_shape, num_recommendations)

        return jsonify({
            'success': True,
            'face_shape': face_shape,
            'hairstyles': hairstyles
        })

    except UnidentifiedImageError:
        logging.error("Invalid image format.")
        return jsonify({'success': False, 'error': 'Invalid image format.'}), 400
    except Exception as e:
        logging.exception("Error processing image")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables
    app.run(debug=True)
