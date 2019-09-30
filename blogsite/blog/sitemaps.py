from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Blog, Categories

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
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
    changefreq = "never"
    priority = 0.5
    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

class CategoriesSitemap(Sitemap): 
    changefreq = "daily"
    priority = 0.9
    def items(self):
        return Categories.objects.all()

