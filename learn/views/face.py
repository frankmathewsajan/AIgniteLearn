import cv2
import mediapipe as mp
import numpy as np
import pyaudio
import struct
import time

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True,
                                  min_detection_confidence=0.5)

# PyAudio parameters for noise detection
CHUNK = 1024  # Buffer size
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate
NOISE_THRESHOLD = 100  # Amplitude threshold for noise detection

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


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
def is_mouth_open(landmarks, height):
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]

    upper_lip_y = upper_lip.y * height
    lower_lip_y = lower_lip.y * height

    return abs(lower_lip_y - upper_lip_y) > 10  # Threshold for mouth opening


# Function to detect noise levels
def detect_noise():
    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_data = struct.unpack(str(CHUNK) + 'h', data)
    amplitude = max(audio_data)
    return amplitude > NOISE_THRESHOLD


# Function to log unusual activities
def log_activity(message):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


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

            # Determine head orientation, eye gaze, and mouth open status
            turn_direction = get_face_turn(face_landmarks.landmark, width, height)
            eye_gaze = get_eye_gaze(face_landmarks.landmark, width, height)
            mouth_open = is_mouth_open(face_landmarks.landmark, height)

            cv2.putText(frame, f'Head Turn: {turn_direction}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f'Gaze: {eye_gaze}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Mouth: {"Open" if mouth_open else "Closed"}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255), 2)

            # Log unusual activities
            if turn_direction != "Forward":
                log_activity(f"Unusual Head Turn: {turn_direction}")
            if eye_gaze != "Looking Forward":
                log_activity(f"Unusual Eye Gaze: {eye_gaze}")
            if mouth_open:
                log_activity("Mouth Opened")

    # Detect noise
    noise_detected = detect_noise()
    cv2.putText(frame, f'Noise: {"Detected" if noise_detected else "Quiet"}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 0), 2)

    if noise_detected:
        log_activity("Unusual Noise Detected")

    cv2.imshow("Proctoring Software", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
stream.stop_stream()
stream.close()
audio.terminate()
cv2.destroyAllWindows()
