from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


class Table(models.Model):
    """Модель столика в ресторане"""
    name = models.CharField(
        verbose_name='Название столика',
        max_length=100
    )
    seats = models.IntegerField(
        verbose_name='Количество мест'
    )
    location = models.CharField(
        verbose_name='Расположение',
        max_length=200
    )

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'

    def __str__(self):
        """Возвращает строковое представление столика"""
        return f'{self.name} ({self.seats} мест) - {self.location}'


class Reservation(models.Model):
    """Модель бронирования столика"""
    customer = models.CharField(
        verbose_name='Имя клиента',
        max_length=200
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Столик'
    )
    reservation = models.DateTimeField(
        verbose_name='Время бронирования'
    )
    duration = models.IntegerField(
        verbose_name='Длительность (минуты)',
        null=False,
        blank=False,
        validators=[
            MinValueValidator(
                30,
                message='Минимальная длительность бронирования - 30 минут'
            ),
            MaxValueValidator(
                240,
                message='Максимальная длительность бронирования - 4 часа'
            )
        ]
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def clean(self):
        """Проверяет пересечение бронирований для одного столика"""
        overlapping_reservations = Reservation.objects.filter(
            table=self.table,
            reservation__lt=(
                self.reservation + timedelta(
                    minutes=self.duration)
            ),
            reservation__gt=(
                self.reservation - timedelta(
                    minutes=self.duration)
            )
        ).exclude(id=self.id)
        if overlapping_reservations.exists():
            raise ValidationError(
                'Этот столик уже забронирован на выбранное время.'
            )

    def save(self, *args, **kwargs):
        """Сохраняет бронирование с предварительной валидацией"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Возвращает строковое представление бронирования"""
        return (
            f'Бронь для {self.customer} '
            f'на столик {self.table.name} '
            f'на {self.reservation}'
        )
