from django.db import models

# Create your models here.

class MagnetLinks(models.Model):
    title = models.CharField(max_length=1000)
    magnet = models.CharField(max_length=10000)
