from django.db import models
import uuid
from django.contrib.auth.models import User

from culturacyberCore.models import moduleModel, activityModel, taskModel

# Create your models here.

class userModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="extend")
    client = models.ForeignKey('clientModel', on_delete = models.CASCADE)

    is_cultureteam = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class clientModel(models.Model):
    
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)

    name = models.CharField(max_length = 50)
    description = models.TextField(max_length=100)
    teamslink = models.TextField()

    def __str__(self):
        return self.name

    def my_modules(client):
        return moduleModel.objects.filter(client = client)

    def my_activities(client, module):
        return activityModel.objects.filter(client=client, module=module)

    def my_tasks(client, module):
        activities = activityModel.objects.filter(client=client, module=module)
        return taskModel.objects.filter(activity__in=activities)

    def all_client_list():
        return clientModel.objects.all()
    
    def get_client(client):
        return clientModel.objects.get(uuid=client)
    
    def active_model_clients(module):
        return moduleModel.objects.get(uuid=module).client.all()

    def disable_model_clients(module):
        client_active = moduleModel.objects.get(uuid=module).client.all()
        return clientModel.objects.all().exclude(uuid__in=client_active)