# Generated by Django 4.2.16 on 2024-12-05 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_event_date_event_event_time_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(default='2024-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(default='TBD', max_length=255),
            preserve_default=False,
        ),
    ]