# Generated by Django 3.2.8 on 2022-02-22 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_bid_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='owner',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
