# Generated by Django 5.0.4 on 2024-04-27 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_buy_and_sell', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikebuyandsell',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]