from rest_framework import serializers
from .models import Plate


class PlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plate
        fields = ['id', 'plate_number', 'entry_time', 'updated_at', 'image']