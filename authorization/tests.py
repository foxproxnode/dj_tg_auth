from pprint import pprint
from django.test import TestCase
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime
from django.contrib.sessions.backends.db import SessionStore
from authorization.services import (
    add_user_to_session, check_session_exists, update_session_auth_user_id)
from users.models import User


class CheckSessionExistsTest(TestCase):
    def setUp(self):
        self.test_session = Session.objects.create(
            session_key='test_session_key',
            expire_date=timezone.now() + datetime.timedelta(days=1)
        )

    def test_session_exists(self):
        self.assertTrue(check_session_exists('test_session_key'))

    def test_session_does_not_exist(self):
        self.assertFalse(check_session_exists('non_existent_session_key'))

    def tearDown(self):
        self.test_session.delete()


class UpdateSessionAuthUserIdTest(TestCase):
    def setUp(self):
        self.test_session = SessionStore()
        self.test_session.create()
        self.session_key = self.test_session.session_key

    def test_update_session_auth_user_id(self):
        new_user_id = 101

        update_session_auth_user_id(self.session_key, new_user_id)

        updated_session = SessionStore(session_key=self.session_key)

        self.assertEqual(updated_session['_auth_user_id'], new_user_id)

    def tearDown(self):
        self.test_session.delete()


class AddUserToSessionTest(TestCase):

    UUID = '123e4567-e89b-12d3-a456-426614174000'

    def test_create_new_user(self):
        uuid = self.UUID
        username = 'testuser'
        first_name = 'Testname'

        # Добавляем нового пользователя
        user = add_user_to_session(
            uuid=uuid, username=username, first_name=first_name)

        # Проверяем, что пользователь был создан
        self.assertTrue(user.id is not None)
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertTrue(user.has_usable_password() is False)

    def test_update_existing_user(self):
        uuid = self.UUID

        # Создаем пользователя с заданным UUID
        existing_user = User.objects.create(uuid=uuid)
        existing_user.set_unusable_password()
        existing_user.save()

        new_username = 'username_updated'
        new_first_name = 'name_updated'

        user = add_user_to_session(
            uuid=uuid, username=new_username, first_name=new_first_name)

        # Проверяем, что пользователь не был создан заново
        self.assertEqual(user.id, existing_user.id)

        # Проверяем что данные не изменились
        self.assertNotEqual(user.username, new_username)
        self.assertNotEqual(user.first_name, new_first_name)
