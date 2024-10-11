# urls.py
from django.urls import path
from .views import SubscriptionAPIView

urlpatterns = [
    path('api/subscription/', SubscriptionAPIView.as_view(), name='subscription_api'),
]
