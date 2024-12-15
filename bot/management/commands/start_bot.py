import logging
from django.core.management.base import BaseCommand
import telebot

from authorization.services import (
    add_user_to_session, check_session_exists, update_session_auth_user_id)
from config.settings import TG_BOT_TOKEN


logger = telebot.logger
telebot.logger.setLevel(logging.WARN)

bot = telebot.TeleBot(TG_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text_content = message.text
    token = text_content.split(' ')[-1]

    if check_session_exists(token):

        user = add_user_to_session(
            uuid=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name)

        update_session_auth_user_id(
            session_key=token,
            new_user_id=user.pk,
        )
        response_message = "✅ Вы успешно авторизовались на сайте \n🌐 Можете вернуться на сайт"
        bot.send_message(message.chat.id, response_message)
    else:
        bot.reply_to(message, "⚠️ Ошибка авторизации, токен не актуален!")


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        bot.infinity_polling()
