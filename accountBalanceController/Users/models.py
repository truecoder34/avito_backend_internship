from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
# Create your models here.
# Creates custom user model. Which is inhereted  from base django user model. And can be extended with additional fields

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(_('Phone'), help_text=_('Users phone number'), max_length=13,
                            null=False, blank=False, unique=True )

    def __str__(self):
        return f"{self.first_name} {self.last_name} : id - {self.id}"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip().title()