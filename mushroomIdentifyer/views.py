import json
from django.http import HttpResponse, JsonResponse
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

