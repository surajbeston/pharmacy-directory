# Generated by Django 2.2.1 on 2019-06-24 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0018_medicine_info_added_composition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine_info',
            name='identification',
            field=models.CharField(max_length=200),
        ),
    ]
