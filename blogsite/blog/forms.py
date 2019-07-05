"""Creating forms for Frontend"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce import TinyMCE
from .models import Blog, Categories
    
class TinyMCEWidget(TinyMCE):
    """Impoting TinyMCE"""
    def use_required_attribute(self, *args):
        return False

class DateInput(forms.DateInput):
    """Changing date type"""
    input_type = 'date'

CHOICES = [
    ('Gaming', 'Gaming'),
    ('Programming', 'Programming'),
    ('Art', 'Art'),
    ('Science', 'Science'),
    ('Sport', 'Sport'),
    ('Politics', 'Politics'),
]

class PostForm(forms.ModelForm):
    """Form that lets users create Blog"""
    class Meta:
        model = Blog
        fields = ['headline', 'content', 'blog_slug']

class CtgForm(forms.ModelForm):
    """Form that lets users create Blog"""
    class Meta:
        model = Categories
        fields = ['category_name']