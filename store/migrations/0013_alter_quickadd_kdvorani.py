# Generated by Django 4.2.7 on 2023-12-24 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_quickadd_created_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quickadd',
            name='kdvOrani',
            field=models.PositiveIntegerField(default=0),
        ),
    ]