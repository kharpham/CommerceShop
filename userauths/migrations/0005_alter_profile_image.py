# Generated by Django 5.0.7 on 2024-09-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0004_alter_contactus_options_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='anonymous.webp', upload_to='image'),
        ),
    ]
