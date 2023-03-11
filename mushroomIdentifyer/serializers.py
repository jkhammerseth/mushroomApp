from rest_framework import serializers
from .models import Mushroom


class MushroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mushroom
        fields = ['id', 'name', 'latin_name' ,'description', 'edible', 'poisonous', 'area', 'image_url']