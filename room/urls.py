from django.urls import path

from .views import OrderTask

urlpatterns = [
    path('order', OrderTask.as_view()),
    path('order/<str:pk>', OrderTask.as_view()),
]
