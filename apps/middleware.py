from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from apps.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse


@database_sync_to_async
def get_user(token):
    try:
        access_token = AccessToken(token)
        return User.objects.get(id=access_token["user_id"])
    except Exception:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        scope["user"] = await get_user(token) if token else AnonymousUser()
        return await self.inner(scope, receive, send)



class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            device = user.devices.first()
            last_active = device.last_active or now()
            if now() - last_active > timedelta(days=7):
                return JsonResponse({
                    "message": "Sizning qurilmangiz 7 kundan beri aktiv emas. Iltimos, qayta login qiling."}
                )
        else:
            print(f"Anonymous User - {request.method} {request.path}")

        response = self.get_response(request)
        return response
