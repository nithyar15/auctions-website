# Generated by Django 3.2.8 on 2022-02-20 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20220220_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('bidder', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Make_bid',
        ),
    ]
