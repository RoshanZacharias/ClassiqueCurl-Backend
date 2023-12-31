# Generated by Django 4.2.7 on 2023-12-19 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0027_reimbursedamount'),
        ('salon', '0021_timeslot_is_booked'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sendername', models.TextField(blank=True, max_length=100, null=True)),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='booking.order')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='salon.hairsalon')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='room',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
