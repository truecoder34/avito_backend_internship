from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Creates custom user model. Which is inhereted  from base django user model. And can be extended with additional fields
class CustomUser(AbstractUser):
    team = models.CharField(blank=True, max_length=120)