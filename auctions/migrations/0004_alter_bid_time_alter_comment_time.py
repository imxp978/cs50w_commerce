# Generated by Django 4.2.6 on 2023-11-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bid_time_alter_comment_time_alter_listing_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]