""" Testing and debugging blogsite """

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog, Categories
from . import views
from .forms import myUserCreationForm 


class BlogTestCase(TestCase):
    def create_Categories(self):
        return Categories.objects.create( category_name = 'Gaming',
                                    category_description = 'Test desc', 
                                    photo = '',
                                    category_slug = 'gaming'
                                    )
    
    def create_Blog(self):
        user = User.objects.create( first_name = 'Test_name_1',
                                    last_name = 'Test_name_2',
                                    email = 'test@gmail.com',
                                    username = 'Test_username',
                                    password = 'testpassword')
       
        return Blog.objects.create( headline = 'New Test headline', 
                                    pub_date = timezone.now(), 
                                    content = 'Test content',
                                    category_name = self.create_Categories(),
                                    img_name = 'test_image',
                                    blog_slug = 'newtestheadline',
                                    image = '',
                                    author = user)

    def test_blog_creation(self):
        '''Testing models.py '''
        b = self.create_Blog()
        c = self.create_Categories()
        self.assertTrue(isinstance(b, Blog))
        self.assertEqual(b.__str__(), b.headline)
        self.assertEqual(c.__str__(), c.category_name)

    #--TESTING VIEWS.PY--
    #Index
    def test_blog_views_index(self):
        '''Testing index page at views.py'''
        c = self.create_Categories()
        url = reverse('index')
        resp = self.client.get(url)
        
        self.assertEqual(resp.status_code, 200)
        resp_decoded = resp.content.decode()
        self.assertIn(c.category_name, resp_decoded)
    
    #Register
    def test_blog_views_register_get(self):
        
        #Working with get method
        b = self.create_Blog()
        url = reverse('register')
        resp_get = self.client.get(url)

        self.assertEqual(resp_get.status_code, 200)
    
    def test_blog_views_register_post(self):
        #Working with post method
        url = reverse('register')
        resp_post = self.client.post(url)
        self.assertEqual(resp_post.status_code, 200)
        
    def test_blog_views_register_form(self): 
        register_form = myUserCreationForm(data={
            'first_name':"Test_name_new",
            'last_name':"Test_name_2",
            'email':"test@gmail.com",
            'username':"Test_username_new",
            'password1': "testpassword123",
            'password2': "testpassword123", }
        )
        print('\n Register form errors: ',register_form.errors)
        print('\n Register non field form errors: ',register_form.non_field_errors)
            
        url = reverse('register')
        resp_post = self.client.get(url)

        self.assertTrue(register_form.is_valid())
        self.assertEqual(register_form.cleaned_data['username'], "Test_username_new")
        self.assertEqual(register_form.cleaned_data['password1'], "testpassword123")

        self.assertRedirects(resp_post, '/index/', status_code=302, target_status_code=200, 
        msg_prefix='', fetch_redirect_response=True)
        '''
        self.assertEqual(form.first_name, "Test_name_new")
        self.assertEqual(form.last_name, "Test_name_2")
        self.assertEqual(form.email, "test@gmail.com")
        self.assertEqual(form.username, "Test_username_new")
        self.assertEqual(form.check_password('testpassword123'), True)
        '''
# Create your tests here.
