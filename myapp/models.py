from turtle import title
from django.db import models
from datetime import datetime 
import uuid 
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Goods(models.Model):
    name= models.CharField(max_length=100)
    details= models.CharField(max_length=200)



class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=50)
    details=models.CharField(max_length=10000)
    created=models.DateTimeField(default=datetime.now,blank=True )

class Comment(models.Model):
    content=models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created=models.DateTimeField(default=datetime.now,blank=True )