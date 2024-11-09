from django.urls import path
from .consumers import FrameProcessorConsumer

websocket_urlpatterns = [
    path('ws/process-frame/', FrameProcessorConsumer.as_asgi()),
]
