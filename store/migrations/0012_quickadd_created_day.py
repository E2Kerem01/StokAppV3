# Generated by Django 4.2.7 on 2023-12-24 16:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='quickadd',
            name='created_day',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
