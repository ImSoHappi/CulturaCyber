from django.db import models
import uuid
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class postModel(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    title = models.CharField(max_length=80)
    postimg = models.FileField()
    contentbody = RichTextUploadingField()

    def __str__(self):
        return self.title

class attachedModel(models.Model):
    post = models.ForeignKey('postModel', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length = 100)
    file = models.FileField(blank=True)