"""Functions for admin page"""

from django.contrib import admin
from tinymce.widgets import TinyMCE
from django import forms
from django.db import models
from .models import Blog, Categories


class BlogAdmin(admin.ModelAdmin):
    """fieldsets: setting up order of fields in admin page"""
    fieldsets = [
        ("Title/date", {"fields": ["headline", "pub_date"]}),
        ("Author", {"fields": ["author"]}),
        ("Blog slug", {"fields": ["blog_slug"]}),
        ("Category", {"fields": ["category_name"]}),
        ("Image", {"fields":["img_name", "image"]}),
        ("Content", {"fields":["content"]}),
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

admin.site.register(Categories)
admin.site.register(Blog, BlogAdmin)
