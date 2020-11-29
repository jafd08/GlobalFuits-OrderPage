# Generated by Django 2.2.5 on 2020-09-14 06:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0012_auto_20200823_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 14, 6, 27, 5, 681070, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(default='Abierto', max_length=150, unique=True),
        ),
    ]
