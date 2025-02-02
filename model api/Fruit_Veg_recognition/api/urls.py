from django.urls import path
from .views import PredictFoodView

urlpatterns = [
    path('predict/', PredictFoodView.as_view(), name='predict'),
    #path('', index),  # Default route for root URL
]

