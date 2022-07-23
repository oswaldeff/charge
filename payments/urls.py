from django.urls import path
from .views import PointListCreateAPIView, ChargeListCreateAPIView


urlpatterns = [
    path('point', PointListCreateAPIView.as_view()),
    path('charge', ChargeListCreateAPIView),
]
