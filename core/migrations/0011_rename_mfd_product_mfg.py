# Generated by Django 5.0.7 on 2024-07-28 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_product_life_alter_product_stock_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='mfd',
            new_name='mfg',
        ),
    ]
