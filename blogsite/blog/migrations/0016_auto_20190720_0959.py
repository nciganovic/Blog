# Generated by Django 2.2 on 2019-07-20 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_merge_20190719_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='media/blog/amer.jpg', upload_to='media/blog'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='category_name',
            field=models.CharField(choices=[('Gaming', 'Gaming'), ('Art', 'Art'), ('Programming', 'Programming'), ('Science', 'Science'), ('Politics', 'Politics'), ('Sport', 'Sport')], max_length=200),
        ),
    ]
