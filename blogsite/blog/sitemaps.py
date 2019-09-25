from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Blog, Categories

class StaticViewSitemap(Sitemap):
    def items(self):
        working_url = ['index','register', 'login', 
                        'logout',  'create_blog', 
                        'my_blogs', 
                        'my_info', 'change_info',
                        'contact', 'stats', 'premium', 'charge']
        return working_url

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    def items(self):
        return Blog.objects.all()

class CategoriesSitemap(Sitemap): 
    def items(self):
        return Categories.objects.all()
