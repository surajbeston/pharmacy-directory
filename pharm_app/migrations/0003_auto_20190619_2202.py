# Generated by Django 2.2.1 on 2019-06-19 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0002_auto_20190619_2140'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='pharma_users',
            new_name='pharma',
        ),
        migrations.RenameModel(
            old_name='general_users',
            new_name='users',
        ),
    ]