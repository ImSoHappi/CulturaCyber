from django.db import models
import uuid, random
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.

ACTIVITY_STATUS = (
    (0, 'Terminada'),
    (1, 'En Proceso'),
    (2, 'En Espera')
)

TASK_STATUS = (
    (0, 'Terminada'),
    (1, 'En Proceso'),
    (2, 'Corregida'),
    (3, 'Rechazada'),
)

class moduleModel(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)

    name = models.CharField(max_length=100, unique=True)
    icon = models.TextField(null=True, blank=True)
    description = models.TextField()
    client = models.ManyToManyField('culturacyberAuth.clientModel', blank=True)

    def __str__(self):
        return self.name

    def get_all_modules():
        return moduleModel.objects.all()
    
    def get_module(module):
        return moduleModel.objects.get(uuid=module)
    

class activityModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)

    name = models.CharField(max_length=100)
    client = models.ForeignKey('culturacyberAuth.clientModel', on_delete=models.CASCADE)
    module = models.ForeignKey('moduleModel', to_field='uuid', on_delete= models.CASCADE)
    description = models.TextField(max_length=400)
    activity_status = models.IntegerField(choices = ACTIVITY_STATUS, default=2)
    programmed_date = models.DateField()

    def __str__(self):
        return self.name

    def get_next_activity(current_activity, client, module):

        flag = False
        activities = activityModel.objects.filter(client=client, module=module)

        for activity in activities:
            if flag:
                return activity
            if current_activity == activity:
                flag = True

        if flag:
            return "finish"

    def first_activity(module, client):
        flag = True
        if activityModel.objects.filter(module=module, client=client):
            flag = False
        return flag

    def get_activity(activity):
        return activityModel.objects.get(pk=activity)
    
    def get_activity_by_month(month, year):
        return activityModel.objects.filter( Q(created_at__year = year) & Q( created_at__month = month))

class taskModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)
    
    name = models.CharField(max_length=100)
    activity = models.ForeignKey('activityModel', on_delete = models.CASCADE)
    task_status = models.IntegerField(choices = TASK_STATUS, default=1)
    teamslink = models.TextField()

    def __str__(self):
        return self.name

    def all_task_finish(activity):
        task_list = taskModel.objects.filter(activity=activity)
        for task in task_list:
            if task.task_status != 0:
                return False
                break
        return True

    def rejected_tasks():
        today = timezone.now()
        last_monday = today - timedelta(days = today.weekday())
        return taskModel.objects.filter(task_status=3, created_at__range=[last_monday, today])

    def inprocess_tasks():
        today = timezone.now()
        last_monday = today - timedelta(days = today.weekday())
        return taskModel.objects.filter( Q(task_status=1) | Q(task_status=2), created_at__range=[last_monday, today] )

    def finished_tasks():
        today = timezone.now()
        last_monday = today - timedelta(days = today.weekday())
        return taskModel.objects.filter(task_status=0, created_at__range=[last_monday, today])

    