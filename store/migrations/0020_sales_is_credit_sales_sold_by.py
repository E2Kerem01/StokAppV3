# Generated by Django 4.2.7 on 2024-01-05 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_quickadd_name_alter_quickadd_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='is_credit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sales',
            name='sold_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_by_person', to='store.salesperson'),
        ),
    ]
