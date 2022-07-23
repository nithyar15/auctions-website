from django.contrib.auth.models import AbstractUser
from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    image = models.ImageField()
    owner = models.CharField(max_length=64)
    status = models.CharField(max_length=10)
    category = models.CharField(max_length=64)

class User(AbstractUser):
    pass
    listings = models.ManyToManyField(Listing, blank=True, related_name="users")

class Bid(models.Model):
    amount = models.IntegerField()
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

class Watchlist(models.Model):
    account = models.CharField(max_length=64)
    list_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list_item")
    on_list = models.CharField(max_length=10)

class Comment(models.Model):
    content = models.CharField(max_length = 280)
    usr_account = models.CharField(max_length=64)
    comment_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_item")