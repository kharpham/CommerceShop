# Generated by Django 5.0.7 on 2024-08-20 02:39

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='This is the new product', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='specifications',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='This is the new vendor', null=True),
        ),
    ]