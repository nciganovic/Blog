# Generated by Django 2.2 on 2019-08-26 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='photo',
        ),
        migrations.AddField(
            model_name='categories',
            name='image',
            field=models.ImageField(default='blog/media/blog/amer.jpg', upload_to='ctg_image'),
        ),
    ]