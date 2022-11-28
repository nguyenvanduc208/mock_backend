from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager

#password default = ABCabc123456

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=100)
    is_admin = models.BooleanField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'is_admin']

    objects = UserManager()

    def __str__(self):
        return self.email