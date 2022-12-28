# Generated by Django 4.1.4 on 2022-12-20 00:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('regstats', '0007_geographymappings_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geography',
            name='lst_updt_ts',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='geographymappings',
            name='lst_updt_ts',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='metricmappings',
            name='lst_updt_ts',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='metrics',
            name='lst_updt_ts',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='metrictypes',
            name='lst_updt_ts',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
