from django.db import models

# Create your models here.

PROCESS_STATUS = (
    (0, 'Terminada'),
    (1, 'En Proceso'),
)

class MainactivityModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    process_status = models.IntegerField(choices = PROCESS_STATUS, default=1)
    teamslink = models.TextField(blank=True, null=True)
    programmed_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default = False)

    def __str__(self):
        return self.name

class ActivityrecordModel(models.Model):
    main_activity = models.ForeignKey('MainactivityModel', on_delete = models.CASCADE)
    process_status = models.IntegerField(choices = PROCESS_STATUS, default=1)
    process_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default = False)

    def __str__(self):
        return 'Actividad principal: %s - Registro: %s' % (self.main_activity, self.process_name)
