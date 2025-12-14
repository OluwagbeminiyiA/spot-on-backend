from django.urls import path, include

from api import views

urlpatterns = [
    path('spots/', views.SpotListView.as_view(), name='spots'),
    path('spots/create/', views.SpotCreateView.as_view(), name='spot_create'),
    path('review/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('spots/<int:pk>/', views.SpotDetailView.as_view(), name='spot_detail'),
    path('status-reports/create/', views.StatusReportView.as_view(), name='status_report'),
    path('auth/register/', views.register_user, name='register'),
    path('free-halls/', views.ClassFreeRoomsView.as_view(), name='free_halls'),
]
