# Generated by Django 2.0 on 2018-07-31 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Address', '0005_auto_20180731_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='FullName',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Full Name'),
        ),
    ]
