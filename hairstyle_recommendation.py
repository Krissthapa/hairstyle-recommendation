import os
import random
import logging

def load_hairstyles(face_shape):
    base_folder = "static/data/pics"  # Ensure correct base folder path
    folder_path = os.path.join(base_folder, face_shape)  # Only use face shape

    if not os.path.exists(folder_path):
        logging.error(f"Directory does not exist: {folder_path}")
        return []  # Return an empty list if directory is not found

    styles = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return styles

def recommend_styles(face_shape, num_recommendations=3):
    try:
        num_recommendations = int(num_recommendations)  # Ensure num_recommendations is an integer
    except ValueError:
        logging.error(f"Invalid value for num_recommendations: {num_recommendations}")
        return []  # Return an empty list if conversion fails

    if face_shape == "unknown":
        logging.error("Face shape is unknown. No recommendations available.")
        return []  # Return an empty list if face shape is unknown

    styles = load_hairstyles(face_shape)
    if not styles:
        logging.warning("No styles found for the given face shape.")
        return []

    if len(styles) < num_recommendations:
        num_recommendations = len(styles)

    try:
        recommended_styles = random.sample(styles, num_recommendations)
    except ValueError as e:
        logging.error(f"Error selecting random samples: {e}")
        recommended_styles = []

    logging.info(f"Recommended styles: {recommended_styles}")
    return recommended_styles
