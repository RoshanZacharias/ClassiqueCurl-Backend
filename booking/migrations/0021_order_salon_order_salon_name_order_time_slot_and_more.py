# Generated by Django 4.2.7 on 2023-12-12 04:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0021_timeslot_is_booked'),
        ('booking', '0020_remove_order_day_remove_order_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='salon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='salon.hairsalon'),
        ),
        migrations.AddField(
            model_name='order',
            name='salon_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='time_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='salon.timeslot'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='user_email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
