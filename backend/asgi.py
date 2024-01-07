import os
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing as routingchat
from salon import routing as routingNotification

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': URLRouter(routingchat.websocket_urlpatterns + 
            routingNotification.websocket_urlpatterns),

    }
)