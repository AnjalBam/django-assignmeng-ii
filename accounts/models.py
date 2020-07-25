from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class Profile(models.Model):
    profile_img = models.ImageField(upload_to='profile_images/')
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=50)
    key_expires_at = models.DateTimeField()
