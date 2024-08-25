from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length = 100)
    emailid = models.EmailField(max_length=254)

    def __str__(self):
        return self.username
    
# class Dmessage(models.Model):
#     username = models.CharField(max_length=50)
#     message = models.TextField()
#     likes = models.IntegerField(default=0)
#     dislike = models.IntegerField(default=0)
