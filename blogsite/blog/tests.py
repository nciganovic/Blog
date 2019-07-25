""" Testing and debugging blogsite """

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blog, Categories
from . import views

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

    def test_blog_views(self):
        '''Testing views.py '''
        c = self.create_Categories()
        url = reverse('index')
        resp = self.client.get(url)
        
        self.assertEqual(resp.status_code, 200)
        y = resp.content.decode()
        self.assertIn(c.category_name, y)


    

# Create your tests here.
