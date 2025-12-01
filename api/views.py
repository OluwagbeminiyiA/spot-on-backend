from datetime import timezone, datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import Spot, LectureHall
from api.serializers import SpotSerializer, ReviewSerializer, StatusReportSerializer, SpotDetailSerializer, \
    LectureHallSerializer


# Create your views here.

class SpotListView(ListAPIView):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer


class SpotCreateView(CreateAPIView):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    permission_classes = [IsAuthenticated]


class ReviewCreateView(CreateAPIView):
    queryset = Spot.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SpotDetailView(RetrieveAPIView):
    queryset = Spot.objects.all()
    serializer_class = SpotDetailSerializer


class StatusReportView(CreateAPIView):
    queryset = Spot.objects.all()
    serializer_class = StatusReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Authentication API Views

@api_view(['POST'])
def register_user(request):
    """Register a new user"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'detail': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate username
    if User.objects.filter(username=username).exists():
        return Response(
            {'username': ['A user with that username already exists.']},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate email
    if email and User.objects.filter(email=email).exists():
        return Response(
            {'email': ['A user with that email already exists.']},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate password length
    if len(password) < 8:
        return Response(
            {'password': ['Password must be at least 8 characters long.']},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return Response(
            {
                'detail': 'User created successfully',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            },
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


class ClassFreeRoomsView(ListAPIView):
    serializer_class = LectureHallSerializer

    def get_queryset(self):
        now = datetime.now()
        day = now.weekday()
        time = now.time()

        return LectureHall.objects.filter(
            free_halls__day_of_week=day,
            free_halls__start_time__lte=time,
            free_halls__end_time__gte=time
        ).distinct()
