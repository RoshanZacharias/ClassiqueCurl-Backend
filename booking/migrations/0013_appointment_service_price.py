# Generated by Django 4.2.7 on 2023-12-04 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_remove_appointment_service_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='service_price',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
