# Generated by Django 2.2 on 2019-07-18 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20190718_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category_name',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Categories'),
        ),
    ]