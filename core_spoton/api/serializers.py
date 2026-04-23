from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core_spoton.api.models import Spot, Review, StatusReport, LectureHall, ClassFreeRooms, SpotAmenities
from datetime import timedelta
from django.utils import timezone


class ReviewSerializer(ModelSerializer):
    latest_status = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'timestamp', 'user')

    def get_latest_status(self, obj):
        latest = StatusReport.objects.filter(spot=obj).latest('-timestamp').first()

        if latest is None:
            return "Unknown"

        expiration_time = timezone.now() + timedelta(minutes=45)

        if latest.timestamp > expiration_time:
            return f"Unknown but was {latest} {expiration_time} minutes ago"


class StatusReportSerializer(ModelSerializer):
    class Meta:
        model = StatusReport
        fields = '__all__'
        read_only_fields = ('id', 'timestamp', 'user')


class SpotSerializer(ModelSerializer):
    latest_status = serializers.SerializerMethodField()

    reviews = ReviewSerializer(many=True)
    status_reports = StatusReportSerializer(many=True)
    amenities = SpotAmenities()

    class Meta:
        model = Spot
        fields = ['id', 'name', 'location_description', 'capacity_ratings',
                  'is_approved', 'is_quiet', 'operating_hours', 'slug', 'reviews', 'status_reports', 'latest_status', 'amenities']
        read_only_fields = ('id', 'is_approved')

    def get_latest_status(self, obj):
        queryset = StatusReport.objects.filter(spot=obj).order_by('-timestamp').first()
        if queryset is None:
            return "Unknown"
        return queryset.status


class SpotDetailSerializer(SpotSerializer):
    reviews = ReviewSerializer(many=True)
    status_reports = StatusReportSerializer(many=True)

    class Meta:
        model = Spot
        fields = '__all__'


class ClassFreeRoomsSerializer(ModelSerializer):
    class Meta:
        model = ClassFreeRooms
        fields = '__all__'


class LectureHallSerializer(ModelSerializer):
    free_halls = ClassFreeRoomsSerializer(many=True)

    class Meta:
        model = LectureHall
        fields = '__all__'
