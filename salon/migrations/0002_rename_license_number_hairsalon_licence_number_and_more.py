# Generated by Django 4.2.3 on 2023-11-17 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hairsalon',
            old_name='license_number',
            new_name='licence_number',
        ),
        migrations.RemoveField(
            model_name='hairsalon',
            name='license',
        ),
        migrations.AddField(
            model_name='hairsalon',
            name='licence',
            field=models.ImageField(default='default_license.jpg', upload_to='licences/'),
        ),
    ]
