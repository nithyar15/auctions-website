# Generated by Django 3.2.8 on 2022-02-22 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_listing_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='watchlist',
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=64)),
                ('on_list', models.CharField(max_length=10)),
                ('list_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_item', to='auctions.listing')),
            ],
        ),
    ]