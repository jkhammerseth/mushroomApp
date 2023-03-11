from djongo import models
from bson.objectid import ObjectId

# Create your models here.
class Mushroom(models.Model):
    id = ObjectId()
    name = models.CharField(max_length=255)
    latin_name = models.CharField(max_length=255)
    description = models.TextField()
    edible = models.BooleanField(default=False)
    poisonous = models.BooleanField(default=False)
    area = models.CharField(max_length=255)
    image_url = models.URLField()


