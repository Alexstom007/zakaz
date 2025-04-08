from rest_framework import serializers
from django.utils import timezone

from .models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    """Сериализатор для модели столика"""
    name = serializers.CharField(
        label='Название столика',
        help_text='Введите название столика',
        max_length=100
    )
    seats = serializers.IntegerField(
        label='Количество мест',
        help_text='Введите количество мест (от 1 до 12)',
        min_value=1,
        max_value=12,
        error_messages={
            'min_value': 'Минимальное количество мест - 1',
            'max_value': 'Максимальное количество мест - 12'
        }
    )
    location = serializers.CharField(
        label='Расположение',
        help_text='Введите расположение столика',
        max_length=200
    )

    class Meta:
        model = Table
        fields = ['id', 'name', 'seats', 'location']


class ReservationSerializer(serializers.ModelSerializer):
    """Сериализатор для модели бронирования"""
    customer = serializers.CharField(
        label='Имя клиента',
        help_text='Введите имя клиента',
        max_length=200
    )
    table = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(),
        label='Столик',
        help_text='Выберите столик'
    )
    reservation = serializers.DateTimeField(
        label='Время бронирования',
        help_text='Введите дату и время бронирования (дд.мм.гггг чч:мм)',
        format='%d.%m.%Y %H:%M'
    )
    duration = serializers.IntegerField(
        min_value=30,
        max_value=240,
        label='Продолжительность',
        help_text='Введите продолжительность бронирования '
        'в минутах (от 30 до 240)',
        error_messages={
            'required': 'Поле продолжительность обязательно для заполнения',
            'min_value': 'Минимальная длительность бронирования - 30 минут',
            'max_value': 'Максимальная длительность бронирования - 4 часа'
        }
    )

    class Meta:
        model = Reservation
        fields = [
            'id',
            'customer',
            'table',
            'reservation',
            'duration'
        ]

    def validate(self, data):
        """
        Проверяет, что время бронирования не в прошлом
        """
        if data['reservation'] < timezone.now():
            raise serializers.ValidationError(
                'Время бронирования не может быть в прошлом'
            )
        return data
