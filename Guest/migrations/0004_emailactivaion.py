# Generated by Django 2.0 on 2018-05-03 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0003_remove_user_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailActivaion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('key', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('activated', models.BooleanField(default=False)),
                ('forced_expired', models.BooleanField(default=False)),
                ('expires', models.IntegerField(default=7)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
