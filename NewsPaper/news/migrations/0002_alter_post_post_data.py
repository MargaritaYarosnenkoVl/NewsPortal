# Generated by Django 4.1a1 on 2022-06-27 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
