# Generated by Django 4.2.7 on 2023-11-30 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0017_stylist_salon'),
    ]

    operations = [
        migrations.AddField(
            model_name='stylist',
            name='stylist_image',
            field=models.ImageField(default='default_image.jpg', upload_to='stylistImages/'),
        ),
    ]
