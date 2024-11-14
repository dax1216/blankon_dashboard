from django.db import models

class RPGStatus(models.TextChoices):
    BOOKING = "1", "Booking"
    CANCELLATION = "2", "Cancellation"


# Create your models here.
class Booking(models.Model):
    hotel_id = models.IntegerField()
    night_of_stay = models.DateField()
    room_id = models.CharField(max_length=100)
    rpg_status = models.CharField(max_length=5, choices=RPGStatus.choices, default=RPGStatus.BOOKING)
    created_at = models.DateTimeField(auto_now_add=True)

