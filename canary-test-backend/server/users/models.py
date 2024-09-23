from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  client_id = models.CharField(max_length=256, default="")
  selected_repo_id = models.BigIntegerField(default=0)