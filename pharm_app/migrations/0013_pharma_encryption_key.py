# Generated by Django 2.2.1 on 2019-06-22 20:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0012_auto_20190622_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharma',
            name='encryption_key',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]