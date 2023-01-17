from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid

User = get_user_model()



# Create your models here.
class Profile(models.Model):
    """docstring for Profile."""
    usr: str = models.ForeignKey(User, on_delete=models.CASCADE)
    id_usr: int = models.IntegerField()
    Fname:str = models.TextField(blank=True,null=True)
    Mname:str = models.TextField(blank=True,null=True)
    Lname:str = models.TextField(blank=True,null=True)
    Fhone:int = models.IntegerField(blank=True,null=True)
    bio: str = models.TextField(blank=True)
    img_profile = models.ImageField(
        upload_to='ProfileIMG', default="blankprofile.png")
    location: str = models.CharField(max_length=250)
    

    def __str__(self):
        return self.usr.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    user: str = models.CharField(max_length=100)
    image = models.ImageField(upload_to="img_posts")
    caption: str = models.TextField(max_length=250)
    created_at = models.DateTimeField(default=datetime.now)
    Likes: int = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    postid: str = models.CharField(max_length=100)
    username: str = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Followers(models.Model):
    follower: str = models.CharField(max_length=100)
    user: str = models.CharField(max_length=100)

    def __str__(self):
        return self.user