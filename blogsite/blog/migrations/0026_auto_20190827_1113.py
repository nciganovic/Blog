# Generated by Django 2.2 on 2019-08-27 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_auto_20190826_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default=None, upload_to='profile_pic'),
        ),
    ]
