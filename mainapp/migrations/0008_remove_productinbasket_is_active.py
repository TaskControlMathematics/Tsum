# Generated by Django 3.2.7 on 2021-11-03 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_productinbasket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinbasket',
            name='is_active',
        ),
    ]