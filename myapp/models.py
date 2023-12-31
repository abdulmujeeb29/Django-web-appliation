from turtle import title
from django.db import models
from datetime import datetime 
import uuid 
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


# class BlogPostImage(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='blog_images/')


class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=100)
    body=models.TextField()
    created=models.DateTimeField(default=datetime.now,blank=True )
    author =models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content=models.CharField(max_length=100)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created=models.DateTimeField(default=datetime.now,blank=True )

    def __str__(self):
        return self.title