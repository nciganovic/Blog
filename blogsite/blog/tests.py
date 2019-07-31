""" Testing and debugging blogsite """

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .models import Blog, Categories
from .views import index, register
from .forms import myUserCreationForm, myAuthenticationForm


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()

    def create_Categories(self):
        return Categories.objects.create( category_name = 'Gaming',
                                    category_description = 'Test desc', 
                                    photo = '',
                                    category_slug = 'gaming'
                                    )
    
    def create_User(self):
        return User.objects.create( first_name = 'Test_name_1',
                                    last_name = 'Test_name_2',
                                    email = 'test@gmail.com',
                                    username = 'Test_username',
                                    password = 'testpassword')

    def create_Blog(self):
        return Blog.objects.create( headline = 'New Test headline', 
                                    pub_date = timezone.now(), 
                                    content = 'Test content',
                                    category_name = self.create_Categories(),
                                    img_name = 'test_image',
                                    blog_slug = 'newtestheadline',
                                    image = '',
                                    author = self.create_User())

    def test_blog_creation(self):
        '''Testing models.py '''
        b = self.create_Blog()
        c = self.create_Categories()
        self.assertTrue(isinstance(b, Blog))
        self.assertEqual(b.__str__(), b.headline)
        self.assertEqual(c.__str__(), c.category_name)
 
class TestViews(TestCase):
    def setUp(self):
            self.client = Client()
            self.Test_Models = TestModels()
            user = User.objects.create(username='test', email='test@test.com', is_active=True)
            user.set_password('Test1234')
            user.save()

    def test_views_index(self):
        '''Testing index page at views.py'''
        c = self.Test_Models.create_Categories()
        resp = self.client.get(reverse('index'))
        
        self.assertEqual(resp.status_code, 200)
        resp_decoded = resp.content.decode()
        self.assertIn(c.category_name, resp_decoded)
 
    #REGISTER
    def test_views_register_GET(self):
        '''Register GET method'''
        resp_get = self.client.get(reverse('register'))
        self.assertEqual(resp_get.status_code, 200)
    
    def test_views_register_POST(self):
        '''Register POST method'''
        url = reverse('register')
        resp_post = self.client.post(url)
        self.assertEqual(resp_post.status_code, 200)

    def test_view_is_valid_register_form(self):
        register_form = myUserCreationForm(data={
            'first_name':"Test_name_new",
            'last_name':"Test_name_2",
            'email':"test@gmail.com",
            'username':"Test_username_new",
            'password1': "testpassword123",
            'password2': "testpassword123", }
        )
        #print('\n Register form errors: ',register_form.errors)
       #print('\n Register non field form errors: ',register_form.non_field_errors)
        self.assertTrue(register_form.is_valid())
        self.assertEqual(register_form.cleaned_data['username'], "Test_username_new")
        self.assertEqual(register_form.cleaned_data['password1'], "testpassword123")
        self.client.login(username = 'Test_username_new', password="testpassword123")

    def test_views_redirect_register_form(self): 
        '''testing redirecting form'''
        url = reverse('register')
        resp_post = self.client.post(url, {
            'first_name':"Test_name_new",
            'last_name':"Test_name_2",
            'email':"test@gmail.com",
            'username':"Test_username_new",
            'password1': "testpassword123",
            'password2': "testpassword123", })

        self.assertEqual(resp_post.status_code, 302) 
        self.assertRedirects(resp_post, '/', status_code=302, target_status_code=200, 
        msg_prefix='', fetch_redirect_response=True)

    #LOGIN
    def test_views_login_GET(self): 
        url = reverse('login')
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)

    def test_views_login_POST(self): 
        url = reverse('login')
        resp_post = self.client.post(url)
        self.assertEqual(resp_post.status_code, 200)

    def test_view_is_valid_login_form(self):
        login_form = myAuthenticationForm(data={
            'username':"test",
            'password': "Test1234",
             }
        )
        print('\n login_form errors: ',login_form.errors)
        print('\n login_form non field errors: ',login_form.non_field_errors)
        self.assertTrue(login_form.is_valid())
        self.assertEqual(login_form.cleaned_data['username'], "test")
        self.assertEqual(login_form.cleaned_data['password'], "Test1234")
        self.client.login(username='Test_username_new', password="testpassword123")

    def test_views_redirect_login(self): 
        url = reverse('login')
        resp_post = self.client.post(url, {
            'username':"test",
            'password': "Test1234",})

        self.assertEqual(resp_post.status_code, 302) 
        self.assertRedirects(resp_post, '/', status_code=302, target_status_code=200, 
        msg_prefix='', fetch_redirect_response=True)

    #LOGOUT  
    #TODO fix logout test
    def test_views_logout(self):
        url = reverse('logout')
        resp_post = self.client.post(url)
        self.assertEqual(resp_post.status_code, 302)
        self.assertRedirects(resp_post, '/', status_code=302, target_status_code=200, 
        msg_prefix='', fetch_redirect_response=True) 

    def test_single_slug(self):
        #b = self.create_Blog()
        c = self.Test_Models.create_Categories()
        single_slug = 'gaming'
        self.assertEqual(single_slug, c.category_slug)

    def test_create_blog(self): 
        url = reverse('create_blog')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    #TODO make request user so my_blog can work     
    '''
    def test_my_blog(self):
        url = reverse('my_blogs')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    '''
        





        
