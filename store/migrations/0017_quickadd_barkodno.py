# Generated by Django 4.2.7 on 2024-01-02 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_salesperson_alter_sales_date_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='quickadd',
            name='barkodNo',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
