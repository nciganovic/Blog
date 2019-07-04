"""Creating forms for Frontend"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce import TinyMCE
from .models import Blog
    
class TinyMCEWidget(TinyMCE):
    """Impoting TinyMCE"""
    def use_required_attribute(self, *args):
        return False

class DateInput(forms.DateInput):
    """Changing date type"""
    input_type = 'date'

class PostForm(forms.ModelForm):
    """Form that lets users create Blog"""
    
    class Meta:
        model = Blog
        fields = ['headline', 'category_name', 'content', 'blog_slug', 'pub_date']
        widgets = {'pub_date' : DateInput()}
