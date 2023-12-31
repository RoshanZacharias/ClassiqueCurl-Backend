# Generated by Django 4.2.7 on 2023-12-03 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0020_timeslot_salon'),
        ('booking', '0006_appointment_user_email_appointment_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='salon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='salon.hairsalon'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='salon_location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
