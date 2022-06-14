from django.db import models

# Create your models here.

class Search(models.Model):
    keywords = models.CharField(max_length=50)
    initial_date = models.DateField()
    final_date = models.DateField()
    date_col = models.BooleanField(null=True)
    time_col = models.BooleanField(null=True)
    username_col = models.BooleanField(null=True)
    name_col = models.BooleanField(null=True)
    tweet_col = models.BooleanField(null=True)
    photos_col = models.BooleanField(null=True)
    created = models.DateField(auto_now_add=True)
