from django.contrib.auth.models import AbstractUser
from django.db import models



class Listing(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="created")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    starting_bid = models.IntegerField()
    image = models.CharField(blank=True)
    category = models.CharField(max_length=64, blank=True)

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlists")


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()