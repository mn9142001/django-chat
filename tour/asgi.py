import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour.settings')
django.setup()

from .middleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.routes import websocket_urlpatterns
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    )
})
