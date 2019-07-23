"""Elements of Database for Website """

from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

CHOICES = [
    ('Gaming', 'Gaming'),
    ('Art', 'Art'),
    ('Programming', 'Programming'),
    ('Science', 'Science'),
    ('Politics', 'Politics'),
    ('Sport', 'Sport'),
]

class Categories(models.Model): 
    category_name = models.CharField(max_length = 200, choices = CHOICES)
    category_description = models.TextField()
    photo = models.ImageField(upload_to="gallery")
    category_slug = models.CharField(max_length=200)
    def __str__(self):
        """When class Cagories ispy called, category_name will be displayed"""
        return self.category_name

class Blog(models.Model):
    headline = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published', default = timezone.now)
    content = models.TextField()
    category_name = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None)
    img_name = models.CharField(max_length=200)
    blog_slug = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'image', default = 'blog/media/blog/amer.jpg')
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    def __str__(self):
        """When class Blog is called, headlines will be displayed"""
        return self.headline
