import jwt
from django.conf import settings
from .models import User

def get_user_from_token(request):
    token = request.headers.get('Authorization', '').split(' ')[1] if request.headers.get('Authorization') else None
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=payload['id'])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None
