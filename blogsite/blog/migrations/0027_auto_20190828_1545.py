# Generated by Django 2.2 on 2019-08-28 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_auto_20190827_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default=None, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=models.ImageField(default=None, upload_to='ctg_image'),
        ),
    ]
