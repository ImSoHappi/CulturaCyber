from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

USER_ROLE = (  
    (0,'Staff'),
    (1,'Cliente'),
    (2,'Usuarios')
)

class userModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True, related_name="extend")
    role = models.IntegerField(choices= USER_ROLE)

    def __str__(self):
        return self.user.username