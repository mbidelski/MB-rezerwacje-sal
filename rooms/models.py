from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=64, null=True)
    seats = models.IntegerField(null=True)
    projector = models.BooleanField(default=False)


class Reservation(models.Model):
    day = models.DateField(null=True)
    room = models.ForeignKey(Room)
    comment = models.TextField(null=True)
