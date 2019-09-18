"""Functions for admin page"""

from django.contrib import admin
from tinymce.widgets import TinyMCE
from django import forms
from django.db import models
from .models import Blog, Categories, Comment, Profile

class BlogAdmin(admin.ModelAdmin):
    """fieldsets: setting up order of fields in admin page"""
    fieldsets = [
        ("Title/date", {"fields": ["headline", "pub_date"]}),
        ("Author", {"fields": ["author"]}),
        ("Category", {"fields": ["category_name"]}),
        ("Image", {"fields":["image"]}),
        ("Stats", {"fields":["likes", "views"]}),
        ("Content", {"fields":["content"]}),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

admin.site.register(Categories)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Profile)
