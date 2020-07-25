from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class BlogPost(models.Model):
    published_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
