from django.contrib.auth.models import User
from django.db import models

from autoslug import AutoSlugField

CAPACITY_CHOICES = (
    ("SMALL", "Small"),
    ("MEDIUM", "Medium"),
    ("LARGE", "Large"),
)

STATUS_CHOICES = (
    ("EMPTY", "Empty"),
    ("GETTING FULL", "Getting Full"),
    ("COMPLETELY FULL", "Completely Full"),
)

RATING_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

DAY_CHOICES = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
)


# Create your models here.
class Spot(models.Model):
    name = models.CharField(max_length=100)
    location_description = models.TextField()
    capacity_ratings = models.CharField(max_length=100, choices=CAPACITY_CHOICES)
    is_quiet = models.BooleanField(default=False)
    operating_hours = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from="name", default="")

    class Meta:
        ordering = ["is_approved"]
        verbose_name = "spot"
        verbose_name_plural = "spots"
        indexes = [models.Index(fields=["is_approved"])]

    def __str__(self) -> str:
        return f"{self.name} runs from {self.operating_hours}"


class StatusReport(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="status_reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="status_reports")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"{self.user} submitted a status report on {self.spot.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(default=1, choices=RATING_CHOICES)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["rating"]
        verbose_name = "review"
        verbose_name_plural = "reviews"

    def __str__(self) -> str:
        return f"{self.user} submitted a review on {self.spot.name}"


class LectureHall(models.Model):
    name = models.CharField(max_length=100)
    capacity_ratings = models.CharField(max_length=100, choices=CAPACITY_CHOICES)
    has_power_outlets = models.BooleanField(default=False)
    is_quiet = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "lecture hall"
        indexes = [models.Index(fields=["name"])]

    def __str__(self) -> str:
        return self.name + " " + f"{self.is_approved}"


class ClassFreeRooms(models.Model):
    spot = models.ForeignKey(LectureHall, on_delete=models.CASCADE, related_name="free_halls")
    note = models.CharField(blank=True, default="No class", max_length=100)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["day_of_week", "-end_time"]
        indexes = [models.Index(fields=["day_of_week"])]

    def __str__(self) -> str:
        return (
            f"{self.spot.name} is free on ({self.get_day_of_week_display()}) from {self.start_time} to {self.end_time}"
        )


class Amenities(models.Model):
    amenity_name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="amenity_name", unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["amenity_name", "id"]

    def __str__(self) -> str:
        return self.amenity_name


class SpotAmenities(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="amenities")
    amenities = models.ForeignKey(Amenities, on_delete=models.CASCADE, related_name="spots")

    class Meta:
        ordering = ["spot"]

    def __str__(self) -> str:
        return f"{self.spot} has {self.amenities} as amenities"


class SavedSpots(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_spots")
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="saved_by_users")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "spot")
        ordering = ["user"]

    def __str__(self) -> str:
        return f"{self.user} saved {self.spot} spot"
