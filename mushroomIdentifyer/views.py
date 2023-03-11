from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MushroomSerializer
from .models import Mushroom
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from fastai.vision.all import load_learner
from PIL import Image
import io
import numpy as np
import cv2

learn = load_learner("./model/model_v1.pkl")
labels = learn.dls.vocab

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

@ensure_csrf_cookie
def predict_mushroom(request):
    try:
        # Read binary data from request body
        img_data = request.body

        # Convert binary data to numpy array
        img_array = np.frombuffer(img_data, np.uint8)

        # Decode the numpy array as an image using OpenCV
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        pred, pred_idx, probs = learn.predict(img)
        return JsonResponse({'prediction': labels[pred_idx], 'probability': probs[pred_idx].item()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    