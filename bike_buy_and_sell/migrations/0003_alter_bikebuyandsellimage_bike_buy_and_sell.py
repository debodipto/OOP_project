# Generated by Django 5.0.4 on 2024-04-27 03:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_buy_and_sell', '0002_bikebuyandsell_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikebuyandsellimage',
            name='bike_buy_and_sell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='bike_buy_and_sell.bikebuyandsell'),
        ),
    ]