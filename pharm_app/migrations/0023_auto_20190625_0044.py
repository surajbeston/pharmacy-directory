# Generated by Django 2.2.1 on 2019-06-25 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0022_keys_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys_key',
            name='token',
            field=models.CharField(max_length=100),
        ),
    ]