# Generated by Django 2.0 on 2018-07-24 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0005_user_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='full_name',
            new_name='FirstName',
        ),
        migrations.AddField(
            model_name='user',
            name='LastName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]