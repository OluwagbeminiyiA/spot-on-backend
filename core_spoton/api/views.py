import logging
from datetime import datetime
from importlib.util import find_spec

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import cache_page

from jwt.utils import force_bytes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_spoton.api.models import Amenities, LectureHall, SavedSpots, Spot, SpotAmenities
from core_spoton.api.serializers import (
    AmenitiesSerializer,
    LectureHallSerializer,
    ReviewSerializer,
    SavedSpotSerializer,
    SpotAmenitiesSerializer,
    SpotDetailSerializer,
    SpotSerializer,
    StatusReportSerializer,
)

# Create your views here.

logger = logging.getLogger(__name__)


@method_decorator(cache_page(60 * 60), name="dispatch")
class SpotListView(ListAPIView):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    ordering_fields = ["id", "name", "capacity_ratings", "is_quiet"]


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


@method_decorator(cache_page(60 * 60), name="dispatch")
class SpotDetailView(RetrieveAPIView):
    queryset = Spot.objects.all()
    serializer_class = SpotDetailSerializer


class StatusReportView(CreateAPIView):
    queryset = Spot.objects.prefetch_related("status_reports")
    serializer_class = StatusReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Authentication API Views


@api_view(["POST"])
def register_user(request):
    """Register a new user"""
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate username
    if User.objects.filter(username=username).exists():
        return Response(
            {"username": ["A user with that username already exists."]}, status=status.HTTP_400_BAD_REQUEST
        )

    # Ensure it is a school email
    if "@live.unilag.edu.ng" not in email:
        return Response(
            {"detail": "Email address is invalid, enter a University of Lagos valid email address."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    year = datetime.now().year
    year = str(year)[-2:]

    # Checking if the matriculation number is valid in the easiest way possible. It shouldn't be valid after 7 years max mostly because of strike
    try:
        if (int(year) - int(email[:2])) > 7 or (int(year) - int(email[:2])) < 0:
            return Response(
                {
                    "detail": "Invalid email address, this email should no longer be valid. Email us if you think we've made a mistake"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except ValueError:
        pass

    # Validate email
    if email and User.objects.filter(email=email).exists():
        return Response({"email": ["A user with that email already exists."]}, status=status.HTTP_400_BAD_REQUEST)

    # Validate password length
    if len(password) < 8:
        return Response(
            {"password": ["Password must be at least 8 characters long."]}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,
        )

        uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
        token = default_token_generator.make_token(user)

        domain = request.get_host()
        link = (
            f"http://{domain}"
            if find_spec("core_spoton.spoton_backend.local_settings") is not None
            else f"https://{domain}"
        )
        verify_link = f"{link}/api/verify-email/{uid}/{token}/"

        subject = "Verify your SpotOn account"
        message = f"Hi {username},\n\nPlease click the link below to verify your Unilag Email:\n\n{verify_link}"
        send_mail(subject, message, "gagbedejobi@gmail.com", [user.email])
        return Response(
            {"message": "Registration successful! Please check your email to verify your account."},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(cache_page(60 * 60 * 2), name="dispatch")
class ClassFreeRoomsView(ListAPIView):
    serializer_class = LectureHallSerializer
    ordering_fields = ["day_of_week", "end_time"]

    def get_queryset(self):
        now = datetime.now()
        day = now.weekday()

        logger.debug("Free Class rooms have been return successfully")
        return LectureHall.objects.filter(
            free_halls__day_of_week=day,
        ).distinct()


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, User.DoesNotExist, OverflowError, ValueError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified! You can now log in."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Token expired!"}, status=status.HTTP_400_BAD_REQUEST)


class AmenitiesListView(ListAPIView):
    serializer_class = AmenitiesSerializer
    ordering_fields = ["amenity_name", "id"]

    def get_queryset(self):
        queryset = Amenities.objects.all()

        has_power_outlets = self.request.query_params.get("has_power_outlets")
        is_quiet = self.request.query_params.get("is_quiet")
        has_wifi = self.request.query_params.get("has_wifi")

        if has_power_outlets is not None:
            queryset = queryset.filter(has_power_outlets=has_power_outlets.lower() == "true")

        if is_quiet is not None:
            queryset = queryset.filter(is_quiet=is_quiet.lower() == "true")

        if has_wifi is not None:
            queryset = queryset.filter(has_wifi=has_wifi.lower() == "true")

        return queryset


class SpotAmenitiesListView(ListAPIView):
    queryset = SpotAmenities.objects.all()
    serializer_class = SpotAmenitiesSerializer
    ordering_fields = ["spot__name", "amenity__name"]


# TODO: Uncomment the permission_classes in saved spots view and return only saved spots requested by the user
class SavedSpotsListView(ListAPIView):
    serializer_class = SavedSpotSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return SavedSpots.objects.filter(user__id=self.request.user.id)
        return SavedSpots.objects.filter(user__id=1)


# TODO: Uncomment the permission class in save spot view and change the user id to self.request.user.id in perform_create method to save the spot for the authenticated user
class SaveSpotView(CreateAPIView):
    serializer_class = SavedSpotSerializer
    # permission_classes = [IsAuthenticated]
