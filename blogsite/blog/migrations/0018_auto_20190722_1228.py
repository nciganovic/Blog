# Generated by Django 2.2 on 2019-07-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20190720_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='blog/media/blog/amer.jpg', upload_to='image'),
        ),
    ]