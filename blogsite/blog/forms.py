from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from tinymce import TinyMCE
from .models import Blog, Categories
     
class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ['headline', 'content', 'blog_slug']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['headline'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['blog_slug'].widget.attrs['class'] = 'form-control'

class CtgForm(forms.ModelForm):
    """Form that lets users create Category"""
    class Meta:
        model = Categories
        fields = ['category_name']
    
    def __init__(self, *args, **kwargs):
        super(CtgForm, self).__init__(*args, **kwargs)

        self.fields['category_name'].widget.attrs['class'] = 'form-control'

class myUserCreationForm(UserCreationForm):

    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class myAuthenticationForm(AuthenticationForm):

    class Meta:
        model=User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(myAuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        
