# Generated by Django 4.2.7 on 2023-12-28 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0036_notification_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user_type',
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver_type',
            field=models.CharField(choices=[('customuser', 'CUSTOMUSER'), ('salonuser', 'SALONUSER')], max_length=20, null=True),
        ),
    ]
