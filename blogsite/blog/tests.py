""" Testing and debugging blogsite """

from django.test import TestCase, override_settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .models import Blog, Categories
from .views import index, register
from .forms import myUserCreationForm, myAuthenticationForm


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
    #INDEX
    def test_blog_views_index(self):
        '''Testing index page at views.py'''
        c = self.create_Categories()
        url = reverse('index')
        resp = self.client.get(url)
        
        self.assertEqual(resp.status_code, 200)
        resp_decoded = resp.content.decode()
        self.assertIn(c.category_name, resp_decoded)
    
    #REGISTER
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
        self.assertTrue(register_form.is_valid())
        self.assertEqual(register_form.cleaned_data['username'], "Test_username_new")
        self.assertEqual(register_form.cleaned_data['password1'], "testpassword123")

        '''
        request = HttpRequest()
        request.method = 'POST'

        response = register(request)

        url = reverse('register')
        resp_post = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['location'], '/')
       
        self.assertRedirects(resp_post, '/index/', status_code=302, target_status_code=200, 
        msg_prefix='', fetch_redirect_response=True)
        '''
    #LOGIN
    def test_blog_views_login_get(self): 
        url = reverse('login')
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)

    def test_blog_views_login_post(self): 
        url = reverse('login')
        resp_post = self.client.post(url)
        self.assertEqual(resp_post.status_code, 200)
    
    #TODO fix login test
        '''
    @override_settings(LOGIN_URL='/login/')
    def test_blog_views_login_form(self):
        response = self.client.get(reverse('/'))
        self.assertRedirects(response, '/login/?next=/')
        
        self.failUnlessEqual(self.client.login(username='Test_username',password='testpassword'),True)
        print('\n Login form errors: ',login_form.errors)
        
        self.assertTrue(login_form.is_valid())   
        self.assertEqual(login_form.cleaned_data['username'], "Test_username")
        self.assertEqual(login_form.cleaned_data['password'], "testpassword")
        '''

    #TODO fix logout test
    def test_blog_views_logout(self):
        url = reverse('index')
        resp = self.client.get(url)
        resp = resp.content.decode()

        self.client.logout()
        self.assertIn('Login', resp)

        
