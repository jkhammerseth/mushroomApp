from django.db import models

# Create your models here.
class Mushroom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    edible = models.BooleanField()
    poisonous = models.BooleanField()
    area = models.CharField(max_length=255)
    image_url = models.URLField()