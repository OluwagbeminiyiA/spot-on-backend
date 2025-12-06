from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Spot


# Create your tests here.


class ApiTests(TestCase):
    def setUp(self):
        self.factory = APIClient()
        spot = Spot.objects.create(name='Test Spot',
                                   location_description='Test Description',
                                   capacity_ratings='LARGE',
                                   has_power_outlets=True,
                                   is_quiet=True,
                                   operating_hours='8 A.M - 8 P.M',
                                   is_approved=True,
                                   )

    def testGetSpots(self):
        request = self.factory.get('/api/spots/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Spot.objects.count(), 1)
        self.assertEqual(Spot.objects.first().name, 'Test Spot')

