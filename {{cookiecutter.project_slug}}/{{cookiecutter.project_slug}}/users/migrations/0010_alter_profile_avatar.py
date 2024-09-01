# Generated by Django 5.0.6 on 2024-07-22 11:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_rename_user_profile_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='images/avatar/default.png', upload_to='avatars', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'jfif'], message='allowed extensions only.(jpg, jpeg, png, jfif)')]),
        ),
    ]
