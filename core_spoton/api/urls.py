from django.urls import path

from core_spoton.api import views

urlpatterns = [
    path("spots/", views.SpotListView.as_view(), name="spots"),
    path("spots/create/", views.SpotCreateView.as_view(), name="spot_create"),
    path("review/create/", views.ReviewCreateView.as_view(), name="review_create"),
    path("spots/<int:pk>/", views.SpotDetailView.as_view(), name="spot_detail"),
    path("status-reports/create/", views.StatusReportView.as_view(), name="status_report"),
    path("auth/register/", views.register_user, name="register"),
    path("free-halls/", views.ClassFreeRoomsView.as_view(), name="free_halls"),
    path("verify-email/<uidb64>/<token>/", views.VerifyEmailView.as_view(), name="verify_email"),
    path("amenities/", views.AmenitiesListView.as_view(), name="amenities_list"),
    path("spot-amenities/", views.SpotAmenitiesListView.as_view(), name="spot_amenities"),
    path("spots/saved/", views.SavedSpotsListView.as_view(), name="saved_spots"),
    path("spots/<int:spot_pk>/save/", views.SaveSpotView.as_view(), name="save_spot"),
]
