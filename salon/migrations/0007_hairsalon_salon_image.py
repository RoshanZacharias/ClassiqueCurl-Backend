# Generated by Django 4.2.7 on 2023-11-21 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0006_hairsalon_licence'),
    ]

    operations = [
        migrations.AddField(
            model_name='hairsalon',
            name='salon_image',
            field=models.ImageField(default='default_image.jpg', upload_to='salonImages/'),
        ),
    ]
