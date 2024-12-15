from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from users.models import User


def check_session_exists(session_key):
    try:
        Session.objects.get(session_key=session_key)
        return True
    except Session.DoesNotExist:
        return False


def update_session_auth_user_id(session_key, new_user_id):
    session_store = SessionStore(session_key=session_key)
    session_store['_auth_user_id'] = new_user_id
    session_store.save()


def add_user_to_session(
    uuid: str = '',
    username: str = '',
    first_name: str = '',
) -> User:
    user, created = User.objects.get_or_create(uuid=uuid)
    if created:
        # Устанавливаем недоступный пароль
        user.set_unusable_password()
        if first_name:
            user.first_name = first_name
        if username:
            user.username = username
        user.save()
    return user
