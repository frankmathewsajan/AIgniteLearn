import datetime

import cv2
import mediapipe as mp

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True,
                                  min_detection_confidence=0.5)


# Log unusual activity to a file
def log_activity(activity):
    with open("log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {activity}\n")


# Function to detect face orientation
def get_face_turn(landmarks, width, height):
    nose_tip = landmarks[1]
    left_eye_outer = landmarks[33]
    right_eye_outer = landmarks[263]

    nose_tip_coords = (int(nose_tip.x * width), int(nose_tip.y * height))
    left_eye_coords = (int(left_eye_outer.x * width), int(left_eye_outer.y * height))
    right_eye_coords = (int(right_eye_outer.x * width), int(right_eye_outer.y * height))

    eye_midpoint = ((left_eye_coords[0] + right_eye_coords[0]) // 2, (left_eye_coords[1] + right_eye_coords[1]) // 2)
    horizontal_dist = nose_tip_coords[0] - eye_midpoint[0]

    if horizontal_dist < -20:
        return "Left Turn"
    elif horizontal_dist > 23:
        return "Right Turn"
    return "Forward"


# Function to detect eye gaze direction
def get_eye_gaze(landmarks, width, height):
    left_iris = landmarks[474]
    right_iris = landmarks[469]

    left_iris_x = left_iris.x * width
    right_iris_x = right_iris.x * width

    if left_iris_x < width * 0.45:
        return "Looking Left"
    elif right_iris_x > width * 0.55:
        return "Looking Right"
    return "Looking Forward"


# Function to detect mouth open status
def is_mouth_open(landmarks, width, height):
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]

    upper_lip_y = upper_lip.y * height
    lower_lip_y = lower_lip.y * height

    return abs(lower_lip_y - upper_lip_y) > 10  # Threshold for mouth opening


# Start video capture
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw landmarks and mesh
            for idx, landmark in enumerate(face_landmarks.landmark):
                x, y = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            for connection in mp_face_mesh.FACEMESH_TESSELATION:
                start_idx, end_idx = connection
                start = face_landmarks.landmark[start_idx]
                end = face_landmarks.landmark[end_idx]
                start_coords = int(start.x * width), int(start.y * height)
                end_coords = int(end.x * width), int(end.y * height)
                cv2.line(frame, start_coords, end_coords, (0, 255, 0), 1)

            # Determine head orientation, eye gaze, and mouth open status
            turn_direction = get_face_turn(face_landmarks.landmark, width, height)
            eye_gaze = get_eye_gaze(face_landmarks.landmark, width, height)
            mouth_open = is_mouth_open(face_landmarks.landmark, width, height)

            cv2.putText(frame, f'Head Turn: {turn_direction}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f'Gaze: {eye_gaze}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Mouth: {"Open" if mouth_open else "Closed"}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255), 2)

            # Log unusual activities
            if turn_direction != "Forward":
                log_activity(f"Head Turn Detected: {turn_direction}")
            if eye_gaze != "Looking Forward":
                log_activity(f"Eye Gaze Detected: {eye_gaze}")
            if mouth_open:
                log_activity("Mouth Open Detected")

    cv2.imshow("Proctoring Software", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
