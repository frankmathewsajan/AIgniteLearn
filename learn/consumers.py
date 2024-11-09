import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
import cv2
import numpy as np
from io import BytesIO
from PIL import Image


class FrameProcessorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.room_name = 'frame_processor'
        self.room_group_name = f'frame_{self.room_name}'
        await self.accept()

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection
        pass

    async def receive(self, text_data):
        # Receive frame from the frontend
        text_data_json = json.loads(text_data)
        frame_data = text_data_json['frame']

        # Decode the base64 frame
        frame = self.decode_base64(frame_data)

        # Process the frame (face detection)
        processed_frame = self.process_frame(frame)

        # Send the processed frame back to frontend
        result = self.encode_base64(processed_frame)
        response = {
            'result': result
        }
        await self.send(text_data=json.dumps(response))

    def decode_base64(self, base64_data):
        """Decode base64-encoded image to NumPy array (image)."""
        img_data = base64.b64decode(base64_data.split(',')[1])  # remove the data URL prefix
        img = Image.open(BytesIO(img_data))
        return np.array(img)

    def encode_base64(self, frame):
        """Encode the image back to base64."""
        _, buffer = cv2.imencode('.jpg', frame)
        return f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}'

    def process_frame(self, frame):
        """Process the frame and detect faces."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame
