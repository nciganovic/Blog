""" Testing and debugging blogsite """

from django.test import TestCase, Client, RequestFactory
from django.utils import timezone
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .models import Blog, Categories, Comment, Profile
from .views import index, register, create_blog, my_blogs, single_slug
from .forms import myUserCreationForm, myAuthenticationForm, PostForm


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()

    def create_Categories(self):
        return Categories.objects.create( category_name = 'Gaming',
                                    category_description = 'Test desc', 
                                    image = 'image',
                                    category_slug = 'gaming'
                                    )
    
    def create_User(self):
        return User.objects.create( first_name = 'Test_name_1',
                                    last_name = 'Test_name_2',
                                    email = 'test@test.com',
                                    username = 'test_user',
                                    password = 'Test1234',
                                    is_active=True)
    
    def create_Blog(self):
        u = User.objects.get(username = 'test_user', password = 'Test1234')
        return Blog.objects.create( headline = 'New Test headline', 
                                    pub_date = timezone.now(),
                                    author = u, 
                                    content = 'Test content',
                                    category_name = self.create_Categories(),
                                    img_name = 'test_image',
                                    blog_slug = 'newtestheadline',
                                    image = 'image',)
                                  
    def create_Comment(self):
        b = Blog.objects.get(headline = 'New Test headline')
        u = User.objects.get(username = 'test_user', password = 'Test1234')
        return Comment.objects.create(comment_text='this is comment text',
                                      author=u,
                                      blog=b)
    
    def test_blog_creation(self):
        user = self.create_User()
        b = self.create_Blog()
        c = self.create_Categories()
        comment = self.create_Comment()
        self.assertTrue(isinstance(b, Blog))
        self.assertEqual(b.__str__(), b.headline)
        self.assertEqual(c.__str__(), c.category_name)
        self.assertEqual(b.get_absolute_url(), f'/{b.blog_slug}')
        self.assertEqual(c.get_absolute_url(), f'/{c.category_slug}')
        self.assertEqual(comment.__str__(), '{}:{}'.format(b.headline, str(user.username)) )

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.Test_Models = TestModels()

        self.premium_user_1 = User.objects.create(first_name = 'tpu1',last_name = 'tpu1',email = 'tpu1@test.com',username = 'tpu1',password = 'Test1234',is_active=True)
        self.premium_user_2 = User.objects.create(first_name = 'tpu2',last_name = 'tpu2',email = 'tpu2@test.com',username = 'tpu2',password = 'Test1234',is_active=True)
        self.premium_user_3 = User.objects.create(first_name = 'tpu3',last_name = 'tpu3',email = 'tpu3@test.com',username = 'tpu3',password = 'Test1234',is_active=True)
        self.premium_user_4 = User.objects.create(first_name = 'tpu4',last_name = 'tpu4',email = 'tpu4@test.com',username = 'tpu4',password = 'Test1234',is_active=True)
        self.premium_user_5 = User.objects.create(first_name = 'tpu5',last_name = 'tpu5',email = 'tpu5@test.com',username = 'tpu5',password = 'Test1234',is_active=True)

        self.get_premium_user_1 = User.objects.get(first_name='tpu1')
        self.get_premium_user_2 = User.objects.get(first_name='tpu2')
        self.get_premium_user_3 = User.objects.get(first_name='tpu3')
        self.get_premium_user_4 = User.objects.get(first_name='tpu4')
        self.get_premium_user_5 = User.objects.get(first_name='tpu5')

        get_profile_1 = Profile.objects.get(user=self.get_premium_user_1)
        get_profile_1.premium = True
        if get_profile_1.premium == True:
            print('tpu1 is premium')
        else:
            print('tpu1 is NOT premium') 

        get_profile_2 = Profile.objects.get(user=self.get_premium_user_2)
        get_profile_2.premium = True
        if get_profile_2.premium == True:
            print('tpu2 is premium')
        else:
            print('tpu2 is NOT premium')

        get_profile_3 = Profile.objects.get(user=self.get_premium_user_3)
        get_profile_3.premium = True
        if get_profile_3.premium == True:
            print('tpu3 is premium')
        else:
            print('tpu3 is NOT premium')

        get_profile_4 = Profile.objects.get(user=self.get_premium_user_4)
        get_profile_4.premium = True
        if get_profile_4.premium == True:
            print('tpu4 is premium')
        else:
            print('tpu4 is NOT premium')

        get_profile_5 = Profile.objects.get(user=self.get_premium_user_5)
        get_profile_5.premium = True
        if get_profile_5.premium == True:
            print('tpu5 is premium')
        else:
            print('tpu5 is NOT premium')
    
        self.category = self.Test_Models.create_Categories()

        self.blog_1 = Blog.objects.create(headline='New Test headline', pub_date=timezone.now(), author=self.premium_user_1, content='Test content', category_name=self.category, img_name='test_image', blog_slug='newtestheadline1', image='image',)
        self.blog_2 = Blog.objects.create(headline='New Test headline', pub_date=timezone.now(), author=self.premium_user_2, content='Test content', category_name=self.category, img_name='test_image', blog_slug='newtestheadline2', image='image',)
        self.blog_3 = Blog.objects.create(headline='New Test headline', pub_date=timezone.now(), author=self.premium_user_3, content='Test content', category_name=self.category, img_name='test_image', blog_slug='newtestheadline3', image='image',)
        self.blog_4 = Blog.objects.create(headline='New Test headline', pub_date=timezone.now(), author=self.premium_user_4, content='Test content', category_name=self.category, img_name='test_image', blog_slug='newtestheadline4', image='image',)
        self.blog_5 = Blog.objects.create(headline='New Test headline', pub_date=timezone.now(), author=self.premium_user_5, content='Test content', category_name=self.category, img_name='test_image', blog_slug='newtestheadline5', image='image',)
   
    def test_index(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
    '''
class TestViews(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
        self.Test_Models = TestModels()
        self.user = self.Test_Models.create_User()
        self.user.set_password('Test1234')
        self.user.save()
        self.create_Categories = self.Test_Models.create_Categories()
    
    def test_views_index(self):
        print('TEST 2 STARTED')
        c = self.Test_Models.create_Categories()
        resp = self.client.get(reverse('index'))
        
        self.assertEqual(resp.status_code, 200)
        resp_decoded = resp.content.decode()
        self.assertIn(c.category_name, resp_decoded)
    
    #REGISTER
    def test_views_register_GET(self):
        resp_get = self.client.get(reverse('register'))
        self.assertEqual(resp_get.status_code, 200)
    
    def test_views_register_POST(self):
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
        #print('\n login_form errors: ',login_form.errors)
        #print('\n login_form non field errors: ',login_form.non_field_errors)
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
    def test_views_logout(self):
        url = reverse('logout')
        resp_post = self.client.post(url)
        self.assertEqual(resp_post.status_code, 302)
        self.assertRedirects(resp_post, '/', status_code=302, target_status_code=200, 
        msg_prefix='', fetch_redirect_response=True) 
    
    #SINGLE_SLUG
    def test_view_single_slug_category(self):
        c = self.Test_Models.create_Categories()
        url = reverse('single_slug', args=(c.category_slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
   
    #TODO fix single_slug for blogs    

    #CREATE_BLOG
    def test_view_create_blog_GET(self): 
        url = reverse('create_blog')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_create_blog_POST(self): 
        url = reverse('create_blog')
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
    
    def test_view_is_valid_create_blog_form(self): 
        c = self.Test_Models.create_Categories()
        blog_post = PostForm(data={
            'headline':"Headline test",
            'category_name': "1",
            'image': "image",
            'img_name': "testimg",
            'content': "Test Content",
            'blog_slug': "testslug",
             }
        )
        #print('\n Blog post errors: ',blog_post.errors)
        #print('\n Blog post field errors: ',blog_post.non_field_errors)
        self.assertTrue(blog_post.is_valid())
        
    def test_view_create_blog_redirect(self): 
        c = self.Test_Models.create_Categories()
        url = reverse('create_blog')
        request = self.request_factory.post(url, {
            'headline':"Headline test",
            'category_name': "1",
            'image': "image",
            'img_name': "testimg",
            'content': "Test Content",
            'blog_slug': "testslug",
             })
        request.user = self.user
        Blog.author = request.user
        response = create_blog(request)
        self.assertEqual(response.status_code, 302) 

        resp_post = self.client.post(url, {
            'headline':"Headline test",
            'category_name': "1",
            'image': "image",
            'img_name': "testimg",
            'content': "Test Content",
            'blog_slug': "testslug",
             })
        self.assertRedirects(resp_post, '/', status_code=302, target_status_code=200, 
        msg_prefix='', fetch_redirect_response=True)
    
    #MY_BLOG     
    def test_my_blog(self):
        url = reverse('my_blogs')
        request = self.request_factory.get(url)
        request.user = self.user
        Blog.author = request.user
        response = my_blogs(request)
        self.assertEqual(response.status_code, 200) 

class SlugTestCase(TestCase):
    def setUp(self):
        Categories.objects.create(  category_name = 'Art',
                                    category_description = 'Test desc', 
                                    image = 'image',
                                    category_slug = 'art')
        User.objects.create(username='tester', password='tester')
        Blog.objects.create(headline = 'This is title', 
                            pub_date = timezone.now(),
                            author = User.objects.get(username='tester'),
                            content = 'Test content',
                            category_name = Categories.objects.get(category_name = 'Art'),
                            img_name = 'test_image',
                            image = 'image',)
        Blog.objects.create(headline = 'This is title', 
                            pub_date = timezone.now(),
                            author = User.objects.get(username='tester'),
                            content = 'Test content',
                            category_name = Categories.objects.get(category_name = 'Art'),
                            img_name = 'test_image',
                            image = 'image',)
        Comment.objects.create(comment_text='this is comment',
                               author = User.objects.get(username='tester'),
                               blog = Blog.objects.get(blog_slug='this-is-title'))                    
   
    def test_slug(self):
        object_1 = Blog.objects.get(pk=1)
        object_2 = Blog.objects.get(pk=2)
        self.assertEqual(object_1.blog_slug, 'this-is-title')
        self.assertEqual(object_2.blog_slug, 'this-is-title-2')
    '''