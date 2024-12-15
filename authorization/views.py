from pprint import pprint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.sessions.models import Session

from django.contrib.auth import logout
from authorization.services import check_session_exists, update_session_auth_user_id
from bot.services import create_auth_telegram_link
from users.models import User
from config.settings import TG_BOT_NAME


def home_view(request):

    session_key = request.session.session_key
    if not session_key or session_key and not check_session_exists(session_key):
        request.session.create()  # Создаем новую сессию, если ее еще нет
    # request.session.modified = True
    unique_token = request.session.session_key  # Теперь session_key должен быть установлен
    user_id = request.session.get('_auth_user_id')

    if user_id:
        user = User.objects.get(id=user_id)
        print(user)
    else:
        user = None

    telegram_link = create_auth_telegram_link(unique_token, TG_BOT_NAME)
    context = {
        'unique_token': unique_token,
        'user_id': user_id,
        'user': user,
        'telegram_link': telegram_link
    }
    return render(request, 'authorization/login.html', context)


def check_auth_view(request):

    session_key = request.GET.get('token')
    if not session_key:
        return JsonResponse(
            {'ok': False, 'detail': 'The token was not transferred!'},
            status=400,
        )

    try:
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded().get('_auth_user_id', None)
        if user_id:
            return JsonResponse({'ok': True, 'detail': 'Success'}, status=200)
        return JsonResponse({'ok': True, 'detail': 'Unauthorized'}, status=401)
    except Session.DoesNotExist:
        return JsonResponse(
            {'ok': False, 'detail': 'The session does not exist!'},
            status=404,
        )


def logout_view(request):
    logout(request)  # Удаление пользователя из сессии
    return JsonResponse({'detail': 'Successful exit'})
