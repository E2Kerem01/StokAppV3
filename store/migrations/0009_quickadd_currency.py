# Generated by Django 4.2.7 on 2023-12-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_product_delete_category_quickadd_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quickadd',
            name='currency',
            field=models.CharField(choices=[('TRY', 'TRY'), ('USD', 'USD'), ('EUR', 'EUR')], default='TRY', max_length=3),
        ),
    ]
