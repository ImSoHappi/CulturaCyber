from django.db import models
import uuid, random
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.apps import apps


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

ACTIVITIES = (
    (0, 'Poster Conocimiento'),
    (1, 'Poster Actitud'),
    (2, 'Poster Comportamiento'),
    (3, 'Infografía'),
    (4, 'Newsletter'),
    (5, 'Noticia'),
    (6, 'Vídeo'),
    (7, 'Actividad/Ejercicio Phishing'),
    (8, 'Test'),
    (9, 'Prueba'),
    (10, 'Encuesta')
)

class client_module_Model(models.Model):
    client = models.ForeignKey('culturacyberAuth.clientModel', on_delete=models.CASCADE, blank=True, null=True)
    module = models.ForeignKey('moduleModel', to_field='uuid', on_delete= models.CASCADE, blank=True, null=True)
    teamslink = models.TextField(default='-')
    disabled = models.BooleanField(default = False)

    class Meta:
        db_table = "culturacyberCore_moduleModel_client"

    def get_client_module(module, client):
        return client_module_Model.objects.get(module=module, client=client)

    def get_or_create_client_module(module, client):
        try:
            return client_module_Model.objects.get(module=module, client=client)
        except:
            
            new_module = moduleModel.objects.get(uuid=module)
            new_client = apps.get_model('culturacyberAuth.clientModel').objects.get(uuid=client)
            cmm = client_module_Model()
            cmm.client = new_client
            cmm.module = new_module
            cmm.disabled = True
            cmm.save()
            return cmm
        
    
    def get_client_module_list(module):
        return client_module_Model.objects.filter(module=module)
    
    def all_client_module():
        return client_module_Model.objects.all()
    

class moduleModel(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default = False)

    name = models.CharField(max_length=100, unique=True)
    icon = models.TextField(null=True, blank=True)
    description = models.TextField()
    client = models.ManyToManyField('culturacyberAuth.clientModel', blank=True , through='client_module_Model')

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

    name = models.IntegerField(choices=ACTIVITIES, default=0)
    client = models.ForeignKey('culturacyberAuth.clientModel', on_delete=models.CASCADE)
    module = models.ForeignKey('moduleModel', to_field='uuid', on_delete= models.CASCADE)
    description = models.TextField(max_length=400)
    activity_status = models.IntegerField(choices = ACTIVITY_STATUS, default=2)
    programmed_date = models.DateField()

    def __str__(self):
        return self.get_name_display()

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
    updated_for = models.CharField(max_length=100, default="-")

    def __str__(self):
        return self.name

    def get_task(task):
        return taskModel.objects.get(pk=task)

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
        return taskModel.objects.filter( Q(task_status=1) | Q(task_status=2))

    def finished_tasks():
        today = timezone.now()
        last_monday = today - timedelta(days = today.weekday())
        return taskModel.objects.filter(task_status=0, created_at__range=[last_monday, today])

    def get_all_tasks_client(client):
        activity = activityModel.objects.filter(client=client)
        return taskModel.objects.filter(activity__in=activity)

    def get_calendar_task(client):
        active_modules = moduleModel.objects.filter(client=client)
        active_modules = activityModel.objects.filter(module__in=active_modules, client=client)
        active_modules = taskModel.objects.filter(activity__in=active_modules)
        return active_modules
    
    def get_rejected_module_task(module, client):
        activities = activityModel.objects.filter(module=module, client=client)
        return taskModel.objects.filter(activity__in=activities, task_status=3)
    
    def get_finished_module_task(module, client):
        activities = activityModel.objects.filter(module=module, client=client)
        return taskModel.objects.filter(activity__in=activities, task_status=0)

    def get_inprocess_module_task(module, client):
        activities = activityModel.objects.filter(module=module, client=client)
        return taskModel.objects.filter( Q(task_status=1) |  Q(task_status=2), activity__in=activities )
    


    