from django.urls import path
from apps.heal_check.views import HealCheckViewSet


urlpatterns = [
    path('heal-check/', HealCheckViewSet.as_view(), name='heal_check')
]
