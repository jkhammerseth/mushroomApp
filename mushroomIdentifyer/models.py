from djongo import models

# Create your models here.
class Mushroom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    edible = models.BooleanField(default=False)
    poisonous = models.BooleanField(default=False)
    area = models.CharField(max_length=255)
    image_url = models.URLField()


