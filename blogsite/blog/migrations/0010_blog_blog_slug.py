# Generated by Django 2.2 on 2019-05-20 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_blog_img_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_slug',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
