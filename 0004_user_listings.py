# Generated by Django 3.2.8 on 2022-02-20 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_pic_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='users', to='auctions.Listing'),
        ),
    ]