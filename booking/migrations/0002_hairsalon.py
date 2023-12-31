# Generated by Django 4.2.3 on 2023-11-17 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HairSalon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salon_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=20)),
                ('licence', models.ImageField(upload_to='licences/')),
                ('licence_number', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
    ]
