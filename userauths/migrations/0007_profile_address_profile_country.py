# Generated by Django 5.0.7 on 2024-09-26 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0006_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]