# hairstyle-recommendation
# Hairstyle Recommendation System

Welcome to the Hairstyle Recommendation System! This project is an AI-powered application designed to help users find the best hairstyles based on their face shapes. By leveraging face detection and classification, the app suggests hairstyles that complement the user's unique facial features.

## Features

- **Face Detection:** Automatically detect and classify the user's face shape.
- **Hairstyle Recommendations:** Suggests hairstyles that match the detected face shape.
- **User-Friendly Interface:** Simple and intuitive interface for easy navigation and interaction.

## Technologies Used

- **Python:** Main programming language.
- **Flask:** Web framework for building the application.
- **OpenCV:** For face detection.
- **Dlib:** Used for facial landmark detection.
- **Machine Learning:** For classifying face shapes and recommending hairstyles.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/hairstyle-recommendation.git
Navigate to the project directory:
bash
Copy code
cd hairstyle-recommendation
Create a virtual environment:
bash
Copy code
python -m venv venv
Activate the virtual environment:
On Windows:
bash
Copy code
venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source venv/bin/activate
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Usage
Run the application:
bash
Copy code
python app.py
Open your browser and navigate to:
arduino
Copy code
http://localhost:5000
Upload a photo:
The application will detect your face shape and recommend suitable hairstyles.
Project Structure
app.py: Main application file.
face_classification.py: Contains the classify_face_shape function for face shape classification.
static/: Contains static files like CSS, images, etc.
templates/: Contains HTML templates for rendering the web pages.
requirements.txt: Lists all the dependencies required to run the project.
Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any inquiries or questions, feel free to contact me at your.email@example.com.
