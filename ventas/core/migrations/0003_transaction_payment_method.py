# Generated by Django 5.0.6 on 2024-06-22 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(default='efectivo', max_length=50),
        ),
    ]
