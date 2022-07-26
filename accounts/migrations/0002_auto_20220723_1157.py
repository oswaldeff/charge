# Generated by Django 3.2 on 2022-07-23 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='serviceuser',
            options={'ordering': ('-user',), 'verbose_name': '서비스 유저', 'verbose_name_plural': '서비스 유저들'},
        ),
        migrations.RemoveField(
            model_name='serviceuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='serviceuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='유저'),
        ),
    ]
