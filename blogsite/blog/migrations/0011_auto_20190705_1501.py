# Generated by Django 2.2 on 2019-07-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_blog_blog_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category_name',
            field=models.CharField(choices=[('Gaming', 'Gaming'), ('Programming', 'Programming'), ('Art', 'Art'), ('Science', 'Science'), ('Sport', 'Sport'), ('Politics', 'Politics')], max_length=200),
        ),
    ]