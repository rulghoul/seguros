# urls.py
from django.urls import path, include
from .views import SubscriptionAPIView, SuscripcionViewSet
from rest_framework import routers 
  
# import everything from views 
from .views import *
  
# define the router 
router = routers.DefaultRouter() 
  
# define the router path and viewset to be used 
router.register(r'subscripciones', SuscripcionViewSet) 
urlpatterns = [
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription_api'),
    path('', include(router.urls)), 
]
