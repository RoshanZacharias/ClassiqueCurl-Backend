# Generated by Django 4.2.7 on 2023-12-27 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0028_remove_reimbursedamount_timestamp_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]