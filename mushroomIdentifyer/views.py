import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MushroomSerializer
from .models import Mushroom


class MushroomViewSet(viewsets.ModelViewSet):
    queryset = Mushroom.objects.all()
    serializer_class = MushroomSerializer


@api_view(['GET'])
def search_mushrooms(request):
    name = request.query_params.get('name', '')
    mushrooms = Mushroom.objects.filter(name__icontains=name)
    serializer = MushroomSerializer(mushrooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def edible_mushrooms(request):
    mushrooms = Mushroom.objects.filter(edible=True)
    data = {'mushrooms': list(mushrooms.values())}
    return JsonResponse(data)

@api_view(['GET'])
def poisonous_mushrooms(request):
    mushrooms = Mushroom.objects.filter(poisonous=True)
    data = {'mushrooms': list(mushrooms.values())}
    return JsonResponse(data)

@api_view(['DELETE'])
def delete_mushroom(request, mushroom_id):
    with open('mushrooms.json', 'r') as f:
        mushrooms = json.load(f)

    index = -1
    for i, mushroom in enumerate(mushrooms):
        if mushroom['id'] == mushroom_id:
            index = i
            break
        
    if index >= 0:
        del mushrooms[index]
        with open('mushrooms.json', 'w') as f:
            json.dump(mushrooms, f)

        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)

@api_view(['PUT'])
def update_mushroom(request, mushroom_id):
    try:
        mushroom = Mushroom.objects.get(pk=mushroom_id)
    except Mushroom.DoesNotExist:
        return Response(status=400)

    serializer = MushroomSerializer(mushroom, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# Retrieves a list of all mushrooms from the database and 
# 
# returns them as a serialized JSON response

@api_view(['GET'])
def mushroom_list(request):
    mushrooms = Mushroom.objects.all()
    serializer = MushroomSerializer(mushrooms, many=True)
    return JsonResponse(serializer.data, safe=False)