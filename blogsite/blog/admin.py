from django.contrib import admin
from tinymce.widgets import TinyMCE
from django import forms
from .models import Blog,Categories
from django.db import models

class BlogAdmin(admin.ModelAdmin):
	fieldsets = [
		("Title/date", {"fields": ["headline", "pub_date"]}),
        ("Blog slug", {"fields": ["blog_slug"]}),
        ("Category", {"fields": ["category_name"]}),
        ("Image", {"fields":["img_name"]}),
		("Content", {"fields":["content"]}),
	]

	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}
	}

admin.site.register(Categories)
admin.site.register(Blog, BlogAdmin)

