# Generated by Django 2.2 on 2019-08-08 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_blog_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]