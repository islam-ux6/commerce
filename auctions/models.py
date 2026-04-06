from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    title = models.CharField(max_length=64)
    description = models.CharField()
    starting_bid = models.IntegerField()
    image = models.CharField(blank=True)
    category = models.CharField(max_length=64, blank=True)