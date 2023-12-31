# Generated by Django 4.2.7 on 2024-01-02 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0017_quickadd_barkodno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quickadd',
            name='name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='quickadd',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
