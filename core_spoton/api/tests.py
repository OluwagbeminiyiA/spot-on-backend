from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from .models import Spot, LectureHall, ClassFreeRooms

User = get_user_model()


# Create your tests here.


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        spot = Spot.objects.create(name='Test Spot',
                                   location_description='Test Description',
                                   capacity_ratings='LARGE',
                                   is_quiet=True,
                                   operating_hours='8 A.M - 8 P.M',
                                   is_approved=True,
                                   )

        testUser = User.objects.create_user(username='testuser',
                                            email='testemail@email.com',
                                            password='testpassword')

        free_lecture_halls = LectureHall.objects.create(name='Free Lecture Hall',
                                                        capacity_ratings='LARGE',
                                                        has_power_outlets=True,
                                                        is_quiet=True,
                                                        is_approved=True,
                                                        )

        now = datetime.now()
        day = now.weekday()

        class_free_room = ClassFreeRooms.objects.create(spot=free_lecture_halls,
                                                        day_of_week=day,
                                                        start_time='08:00:00',
                                                        end_time='22:00:00',
                                                        )
        class_free_room = ClassFreeRooms.objects.create(spot=free_lecture_halls,
                                                        day_of_week=day,
                                                        start_time='23:00:00',
                                                        end_time='00:00:00',
                                                        )

    def testGetSpots(self):
        request = self.client.get('/api/spots/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Spot.objects.count(), 1)
        self.assertEqual(Spot.objects.first().name, 'Test Spot')
        self.assertEqual(request.data['results'][0]['name'], 'Test Spot')
        self.assertEqual(request.data['results'][0]['capacity_ratings'], 'LARGE')

    def testGetFreeSpots(self):
        request = self.client.get('/api/free-halls/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['results'][0]['name'], 'Free Lecture Hall')
        self.assertEqual(request.data['results'][0]['capacity_ratings'], 'LARGE')
        self.assertEqual(request.data['results'][0]['has_power_outlets'], True)

    def testRegistrationView(self):
        request = self.client.post('/api/auth/register/',
                                   {"username": "username",
                                    "email": "21908908@live.unilag.edu.ng",
                                    "password": "<PASSWORD!>"}, format='json')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['message'],
                         "Registration successful! Please check your email to verify your account.")

    def testRegistrationViewWithWrongEmail(self):
        request = self.client.post('/api/auth/register/',
                                   {"username": "username",
                                    "password": "<PASSWORD>",
                                    "email": "gagbedejobi@gmail"},
                                   format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(request.data['detail'],
                         "Email address is invalid, enter a University of Lagos valid email address.")

    def testRegistrationViewWithOldSchoolEmail(self):
        request = self.client.post('/api/auth/register/',
                                   {"username": "username",
                                    "password": "<PASSWORD>",
                                    "email": "15098675@live.unilag.edu.ng",
                                    }, format='json')

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(request.data['detail'],
                         'Invalid email address, this email should no longer be valid. Email us if you think we\'ve made a mistake')

    def testSaveSpot(self):
        request = self.client.post('/api/spots/1/save/', format='json', data={
            'user': User.objects.first().id,
            'spot': Spot.objects.first().id
        })
        self.client.force_authenticate(user=User.objects.first())
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def testGetSavedSpot(self):
        request = self.client.get('/api/spots/saved/')
        self.client.force_authenticate(user=User.objects.first())
