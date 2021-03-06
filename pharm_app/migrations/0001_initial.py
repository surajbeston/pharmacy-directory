# Generated by Django 2.2.1 on 2019-06-19 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='general_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=200)),
                ('signup_date', models.DateTimeField(auto_now_add=True)),
                ('last_signin', models.DateTimeField(blank=True, null=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='pharma_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=200)),
                ('location_address_1', models.CharField(max_length=200)),
                ('location_address_2', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=300)),
                ('phone', models.IntegerField()),
                ('password', models.CharField(max_length=300)),
                ('pin', models.IntegerField(max_length=5)),
                ('confirmation_token', models.CharField(max_length=100)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
    ]
