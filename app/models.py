from django.db import models


class Plate(models.Model):
    plate_number = models.CharField(max_length=50, unique=True)  # Masalan, 50 belgi
    entry_time = models.TimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    exit_time = models.TimeField(null=True)