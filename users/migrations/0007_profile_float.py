# Generated by Django 3.2 on 2021-05-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_intrests'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='float',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
