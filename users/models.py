from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    uuid = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username
