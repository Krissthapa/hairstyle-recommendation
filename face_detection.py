import cv2
import dlib

# Initialize dlib's face detector (HOG-based) and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def detect_face_landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    all_landmarks = []

    if not faces:
        print("No faces detected.")
        return all_landmarks

    for face in faces:
        shape = predictor(gray, face)
        landmarks = [(p.x, p.y) for p in shape.parts()]
        print(f"Landmarks: {landmarks}")  # Debugging line
        all_landmarks.append(landmarks)

    return all_landmarks  # Return a list of lists containing landmarks for each detected face

def visualize_landmarks(image, landmarks):
    for landmark_set in landmarks:
        for (x, y) in landmark_set:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)  # Draw a circle for each landmark

    cv2.imshow("Landmarks", image)  # Display the image with landmarks
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Load an example image (you can replace this with your own image)
    image_path = "path_to_your_image.jpg"
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image at {image_path}")
    else:
        # Detect facial landmarks
        landmarks = detect_face_landmarks(image)

        # Visualize the landmarks
        if landmarks:
            visualize_landmarks(image, landmarks)
        else:
            print("No landmarks to visualize.")
