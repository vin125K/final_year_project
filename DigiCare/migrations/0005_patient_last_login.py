# Generated by Django 4.0.4 on 2024-03-27 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DigiCare', '0004_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
