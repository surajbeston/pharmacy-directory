# Generated by Django 2.2.1 on 2019-06-19 21:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pharma_users',
            name='confirmation_token',
        ),
        migrations.AddField(
            model_name='pharma_users',
            name='authentication_file',
            field=models.FileField(default=django.utils.timezone.now, upload_to='authentication_files/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pharma_users',
            name='pin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
