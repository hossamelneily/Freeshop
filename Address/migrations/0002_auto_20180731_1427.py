# Generated by Django 2.0 on 2018-07-31 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='ContactNo',
            field=models.CharField(default=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='FullName',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
