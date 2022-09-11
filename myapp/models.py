from turtle import title
from django.db import models
from datetime import datetime 

# Create your models here.

class Goods(models.Model):
    name= models.CharField(max_length=100)
    details= models.CharField(max_length=200)



class Post(models.Model):
    title=models.CharField(max_length=50)
    details=models.CharField(max_length=1000)
    created=models.DateTimeField(default=datetime.now,blank=True )