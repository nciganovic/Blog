# Generated by Django 2.2 on 2019-09-16 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0029_auto_20190907_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='blog_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=models.ImageField(default=None, upload_to='ctg_image'),
        ),
    ]