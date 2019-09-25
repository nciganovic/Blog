"""Elements of Database for Website """

import os
import uuid
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import unique_slug_generator

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
    image = models.ImageField(upload_to="ctg_image", default=None)
    category_slug = models.CharField(max_length=200)
    def __str__(self):
        """When class Cagories is called, category_name will be displayed"""
        return self.category_name

    def get_absolute_url(self):
        return f'/{self.category_slug}'

class Blog(models.Model):
    headline = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    content = models.TextField()
    category_name = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None)
    img_name = models.CharField(max_length=200)
    blog_slug = models.SlugField(max_length = 200, unique=True)
    image = models.ImageField(upload_to = 'image', default=None)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='blog_likes')
    views = models.ManyToManyField(User, blank=True, related_name='blog_views')
    def __str__(self):
        """When class Blog is called, headlines will be displayed"""
        return self.headline

    def get_absolute_url(self):
        return f'/{self.blog_slug}'

class Comment(models.Model):
    comment_text = models.TextField(max_length = 200)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)
    def __str__(self): 
        return '{}:{}'.format(self.blog.headline, str(self.author.username))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_pic', default=None, blank=True)
    premium = models.BooleanField(default=False)
    def __str__(self): 
        return self.user.username

def slug_save(sender, instance, *args, **kwargs):
    if not instance.blog_slug: 
        instance.blog_slug = unique_slug_generator(instance, instance.headline, instance.blog_slug)

pre_save.connect(slug_save, sender=Blog)

def unique_img_name(sender, instance, *args, **kwargs):
    if not instance.img_name: 
        instance.img_name = os.path.basename(instance.image.name)
        
pre_save.connect(unique_img_name, sender=Blog)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()