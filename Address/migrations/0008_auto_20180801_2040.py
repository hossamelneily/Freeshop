# Generated by Django 2.0 on 2018-08-01 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Address', '0007_auto_20180731_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Address_Type',
            field=models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], max_length=250, verbose_name='address_type'),
        ),
    ]