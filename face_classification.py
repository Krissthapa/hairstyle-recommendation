import numpy as np

def classify_face_shape(landmarks):
    if not landmarks or len(landmarks) < 33:  # Ensure there are enough landmarks
        print("Insufficient landmarks.")
        return "unknown"

    landmarks = np.array(landmarks)
    
    try:
        # Define facial features using landmark pairs
        jaw_width = np.linalg.norm(landmarks[0] - landmarks[16])
        cheek_width = np.linalg.norm(landmarks[1] - landmarks[15])
        face_height = np.linalg.norm(landmarks[8] - landmarks[27])
        forehead_width = np.linalg.norm(landmarks[17] - landmarks[26])
        chin_to_forehead_height = np.linalg.norm(landmarks[8] - landmarks[19])
        face_width = np.linalg.norm(landmarks[0] - landmarks[16])
        face_length = np.linalg.norm(landmarks[27] - landmarks[8])
    except IndexError as e:
        print(f"IndexError: {e}")
        return "unknown"

    print(f"Jaw Width: {jaw_width}, Cheek Width: {cheek_width}, Face Height: {face_height}, Forehead Width: {forehead_width}")
    print(f"Chin to Forehead Height: {chin_to_forehead_height}, Face Width: {face_width}, Face Length: {face_length}")

    if cheek_width == 0:
        print("Cheek Width is zero, cannot calculate ratios.")
        return "unknown"
    
    # Calculate ratios
    jaw_to_face_width_ratio = jaw_width / face_width
    cheek_to_face_height_ratio = cheek_width / face_height
    chin_to_face_length_ratio = chin_to_forehead_height / face_length
    forehead_to_cheek_ratio = forehead_width / cheek_width

    print(f"Jaw to Face Width Ratio: {jaw_to_face_width_ratio:.2f}, Cheek to Face Height Ratio: {cheek_to_face_height_ratio:.2f}")
    print(f"Chin to Face Length Ratio: {chin_to_face_length_ratio:.2f}, Forehead to Cheek Ratio: {forehead_to_cheek_ratio:.2f}")

    # Adjusted thresholds for better classification
    if chin_to_face_length_ratio > 0.75 and cheek_to_face_height_ratio < 1.1:
        return "oval"
    elif 0.7 <= cheek_to_face_height_ratio <= 0.9 and jaw_to_face_width_ratio < 0.85:
        return "round"
    elif abs(jaw_to_face_width_ratio - 1) < 0.25 and abs(forehead_to_cheek_ratio - 1) < 0.25:
        return "square"
    elif forehead_to_cheek_ratio > 1.25 and jaw_to_face_width_ratio < 0.85:
        return "heart"
    else:
        # Log debug information for uncertain classifications
        print(f"Uncertain classification: chin_to_face_length_ratio={chin_to_face_length_ratio:.2f}, "
              f"cheek_to_face_height_ratio={cheek_to_face_height_ratio:.2f}, "
              f"jaw_to_face_width_ratio={jaw_to_face_width_ratio:.2f}, "
              f"forehead_to_cheek_ratio={forehead_to_cheek_ratio:.2f}")
        return "unknown"
