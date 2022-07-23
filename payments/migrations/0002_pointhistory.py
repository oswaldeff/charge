# Generated by Django 3.2 on 2022-07-23 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220723_1157'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointHistory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='업데이트날짜')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='포인트 충전금액')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payments.card', verbose_name='결제카드')),
                ('service_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.serviceuser', verbose_name='서비스 유저')),
            ],
            options={
                'verbose_name': '포인트 충전기록',
                'verbose_name_plural': '포인트 충전기록들',
                'ordering': ('-id',),
            },
        ),
    ]
