from django.db import models
from django.contrib.auth.models import User


class FBUser(models.Model):
    # FBUser to keystone is Many-to-one
    keystone_userid = models.OneToOneField(User, on_delete=models.CASCADE)
    fb_userid = models.CharField(max_length=20, unique=True)
    fb_username = models.CharField(max_length=50)
    access_token = models.CharField(max_length=255)
