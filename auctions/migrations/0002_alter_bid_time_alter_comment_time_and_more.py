# Generated by Django 4.2.6 on 2023-11-04 09:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 9, 47, 52, 6069)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 9, 47, 52, 5759)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 9, 47, 52, 5319)),
        ),
    ]