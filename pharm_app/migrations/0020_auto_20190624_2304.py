# Generated by Django 2.2.1 on 2019-06-24 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0019_auto_20190624_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine_composition',
            name='weightage',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
    ]
