import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing as routingchat
from salon import routing as routingNotification

# Load environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django application
django_asgi_app = get_asgi_application()

# Define WebSocket routing for different applications
websocket_application = URLRouter(
    routingchat.websocket_urlpatterns +
    routingNotification.websocket_urlpatterns
)

# Configure the ProtocolTypeRouter
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Use Django for HTTP connections
        'websocket': websocket_application,
    }
)
