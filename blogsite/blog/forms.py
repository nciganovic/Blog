"""Creating forms for Frontend"""
from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from tinymce import TinyMCE
from .models import Blog, Categories, Comment, Profile
     
class TinyMCEWidget(TinyMCE):
    """Impoting TinyMCE"""
    def use_required_attribute(self, *args):
        return False

class DateInput(forms.DateInput):
    """Changing date type"""
    input_type = 'date'

class PostForm(forms.ModelForm):
    category_name = forms.ModelChoiceField(queryset=Categories.objects.all())
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}))
    class Meta:
        model = Blog
        fields = ['headline', 'content', 'category_name', 'image']
        exclude = ['author']
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['headline'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['category_name'].widget.attrs['class'] = 'form-control'
        #self.fields['img_name'].widget.attrs['class'] = 'form-control'
        #self.fields['blog_slug'].widget.attrs['class'] = 'form-control'

class myUserCreationForm(UserCreationForm):

    class Meta:
        model=User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
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

class PostComment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('comment_text',)
    def __init__(self, *args, **kwargs):
        super(PostComment, self).__init__(*args, **kwargs)

        self.fields['comment_text'].widget.attrs['class'] = 'form-control'

class ProfileForm(forms.ModelForm): 
    class Meta: 
        model=Profile
        fields=('bio', 'birth_date', 'image',)      
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['bio'].widget.attrs['class'] = 'form-control'
        self.fields['birth_date'].widget.attrs['class'] = 'form-control'

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['from_email'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['subject'].widget.attrs['class'] = 'form-control'
