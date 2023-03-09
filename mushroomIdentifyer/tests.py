from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Mushroom
import json


class MushroomTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mushroom_data = {
            "name": "Kantarell",
            "description": "Kantarell har gul, traktformet hatt, nedløpende folder og god kantarellukt. Har samme gulfarge på undersiden som oversiden. Avrundet stilk.",
            "edible": "True",
            "poisonous": "False",
            "area": "Norge",
            "image_url": "https://media.snl.no/media/116599/standard_compressed_kantarell_37810.jpg"
        }
        self.response = self.client.post(
            reverse('mushroom-list'),
            data=json.dumps(self.mushroom_data),
            content_type='application/json'
        )

    def test_create_mushroom(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mushroom.objects.count(), 1)
        self.assertEqual(Mushroom.objects.get().name, 'Kantarell')

    def test_get_all_mushrooms(self):
        response = self.client.get(reverse('mushroom-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_mushroom(self):
        mushroom = Mushroom.objects.get()
        response = self.client.get(reverse('mushroom-detail', args=[mushroom.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, mushroom.name)

    def test_update_mushroom(self):
        mushroom = Mushroom.objects.get()
        updated_mushroom_data = {
            'name': 'Boletus',
            'description': 'Brown and meaty',
            'edible': True,
            'poisonous': False,
            'area': 'North America',
            'image_url': 'https://example.com/boletus.jpg'
        }
        response = self.client.put(
            reverse('mushroom-detail', args=[mushroom.id]),
            data=json.dumps(updated_mushroom_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Mushroom.objects.get().name, 'Boletus')

    def test_delete_mushroom(self):
        mushroom = Mushroom.objects.get()
        response = self.client.delete(reverse('mushroom-detail', args=[mushroom.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mushroom.objects.count(), 0)
