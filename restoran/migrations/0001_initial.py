# Generated by Django 4.2.7 on 2025-04-08 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название столика')),
                ('seats', models.IntegerField(verbose_name='Количество мест')),
                ('location', models.CharField(max_length=200, verbose_name='Расположение')),
            ],
            options={
                'verbose_name': 'Столик',
                'verbose_name_plural': 'Столики',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=200, verbose_name='Имя клиента')),
                ('reservation', models.DateTimeField(verbose_name='Время бронирования')),
                ('duration', models.IntegerField(verbose_name='Длительность (минуты)')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='restoran.table', verbose_name='Столик')),
            ],
            options={
                'verbose_name': 'Бронь',
                'verbose_name_plural': 'Брони',
            },
        ),
    ]
