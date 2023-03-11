from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MushroomSerializer
from .models import Mushroom
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class MushroomViewSet(viewsets.ModelViewSet):
    queryset = Mushroom.objects.all()
    serializer_class = MushroomSerializer


@api_view(['GET'])
def search_mushrooms(request):
    name = request.query_params.get('name', '')
    mushrooms = Mushroom.objects.filter(name__icontains=name)
    serializer = MushroomSerializer(mushrooms, many=True)
    return Response(serializer.data)

def edible_mushrooms(request):
    mushrooms = Mushroom.objects.filter(edible=True)
    serializer = MushroomSerializer(mushrooms, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'message': 'No edible mushrooms found.'}, status=404)

def poisonous_mushrooms(request):
    mushrooms = Mushroom.objects.filter(poisonous=True)
    serializer = MushroomSerializer(mushrooms, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'message': 'No poisonous mushrooms found.'}, status=404)