# Generated by Django 5.0.3 on 2024-04-01 04:49

import users.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=users.helpers.RandomFileName('profile')),
        ),
    ]
