# Generated by Django 4.2.7 on 2023-12-13 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0024_rename_date_order_time_slot_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
