# Generated by Django 4.2.7 on 2023-12-06 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0020_timeslot_salon'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]
