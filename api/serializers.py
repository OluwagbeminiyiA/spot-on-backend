from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Spot, Review, StatusReport, LectureHall


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'timestamp', 'user')


class StatusReportSerializer(ModelSerializer):
    class Meta:
        model = StatusReport
        fields = '__all__'
        read_only_fields = ('id', 'timestamp', 'user')


class SpotSerializer(ModelSerializer):
    latest_status = serializers.SerializerMethodField()

    reviews = ReviewSerializer(many=True)
    status_reports = StatusReportSerializer(many=True)

    class Meta:
        model = Spot
        fields = ['id', 'name', 'location_description', 'capacity_ratings', 'has_power_outlets',
                  'is_approved', 'is_quiet', 'operating_hours', 'reviews', 'status_reports', 'latest_status']
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


class LectureHallSerializer(ModelSerializer):
    class Meta:
        model = LectureHall
        fields = '__all__'

