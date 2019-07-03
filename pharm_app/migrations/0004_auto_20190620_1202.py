# Generated by Django 2.2.1 on 2019-06-20 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0003_auto_20190619_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='last_signin',
        ),
        migrations.CreateModel(
            name='users_signin_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_signin', models.DateTimeField(blank=True, null=True)),
                ('last_signin', models.DateTimeField(blank=True, null=True)),
                ('signed_out', models.DateTimeField(blank=True, null=True)),
                ('requested_times', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharm_app.users')),
            ],
        ),
        migrations.CreateModel(
            name='pharma_signin_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_signin', models.DateTimeField(blank=True, null=True)),
                ('last_signin', models.DateTimeField(blank=True, null=True)),
                ('signed_out', models.DateTimeField(blank=True, null=True)),
                ('requested_times', models.IntegerField(default=1)),
                ('pharma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharm_app.pharma')),
            ],
        ),
    ]