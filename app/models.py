from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Platforms(models.Model):

    name = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

class Watchlist(models.Model):

    title = models.CharField(max_length=30)
    storyline = models.CharField(max_length=100)
    platform = models.ForeignKey(Platforms, on_delete=models.CASCADE,related_name="Watch_List")
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reviews(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)]) 
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)  
    desc = models.CharField(max_length=200)
    watchlist = models.ForeignKey(Watchlist,on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "Rating "+ str(self.rating) + " for " + str(self.watchlist.title)
