# Generated by Django 4.2.7 on 2023-12-04 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_appointment_service_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='service_price',
            field=models.IntegerField(null=True),
        ),
    ]
