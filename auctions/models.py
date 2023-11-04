from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name="watchlistuser")
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Listing(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    currentprice = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    activation = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.listing.title
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    time = models.DateTimeField(auto_now_add=True)
    