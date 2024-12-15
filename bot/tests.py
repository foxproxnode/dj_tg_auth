from django.test import TestCase

from bot.services import create_auth_telegram_link


class CreateAuthTelegramLinkTest(TestCase):

    TG_BOT_NAME = 'test_bot'

    def test_create_auth_telegram_link(self):

        user_token = '123456'
        expected_url = f'https://t.me/{self.TG_BOT_NAME}?start={user_token}'

        self.assertEqual(
            create_auth_telegram_link(
                user_token, self.TG_BOT_NAME), expected_url)

    def test_create_auth_telegram_link_empty_token(self):
        user_token = ''
        expected_url = f'https://t.me/{self.TG_BOT_NAME}?start={user_token}'
        self.assertEqual(
            create_auth_telegram_link(
                user_token, self.TG_BOT_NAME), expected_url)
