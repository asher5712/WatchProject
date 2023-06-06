from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    """
    Model to represent streaming platform.
    Contains three attributes 'name', 'about' and 'website'
    """    
    
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        """
        Dunder string method for custom representation of the model object

        Returns:
            str: name of the platform
        """   
        
        return self.name


class WatchList(models.Model):    
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        Dunder string method for custom representation of the model object

        Returns:
            str: title of the watch item
        """        
        
        return self.title
    

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """
        Dunder string method for custom representation of the model object

        Returns:
            str: ratings with watch item title
        """        
        
        return str(self.rating) + ' | ' + self.watchlist.title
    
