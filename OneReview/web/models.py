from django.db import models

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=70)
