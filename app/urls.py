from django.urls import path
from .views import process_plates

urlpatterns = [
    path('process/', process_plates, name='process_plates'),
]