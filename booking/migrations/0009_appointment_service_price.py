# Generated by Django 4.2.7 on 2023-12-04 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_rename_salon_location_appointment_salon_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='service_price',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
