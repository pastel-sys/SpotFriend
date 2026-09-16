from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class User(AbstractUser):
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    birthdate = models.DateField(null=True)
     