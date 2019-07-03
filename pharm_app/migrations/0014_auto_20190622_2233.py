# Generated by Django 2.2.1 on 2019-06-22 22:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_app', '0013_pharma_encryption_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pharma',
            old_name='phone',
            new_name='mobile',
        ),
        migrations.AddField(
            model_name='pharma',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pharma',
            name='authentication_file',
            field=models.CharField(blank=True, max_length=206),
        ),
        migrations.CreateModel(
            name='activation_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_datetime', models.DateTimeField(auto_now_add=True)),
                ('pin', models.DecimalField(decimal_places=0, max_digits=6)),
                ('link_randcode', models.CharField(max_length=50)),
                ('pharmaceutical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharm_app.pharma')),
            ],
        ),
    ]