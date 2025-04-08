from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta

from .models import Table, Reservation
from .serializers import (
    TableSerializer,
    ReservationSerializer,
)


class TableViewSet(viewsets.ModelViewSet):
    """ViewSet для управления столиками"""
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def update(self, request, *args, **kwargs):
        """
        Обновляет существующий столик.
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet для управления бронированиями"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        """
        Создает новое бронирование.
        В случае ошибки возвращает сообщение об ошибке.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        Обновляет существующее бронирование.
        Проверяет доступность столика на новое время.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        new_time = serializer.validated_data.get(
            'reservation', instance.reservation)
        new_duration = serializer.validated_data.get(
            'duration', instance.duration)
        new_table = serializer.validated_data.get('table', instance.table)
        overlapping_reservations = Reservation.objects.filter(
            table=new_table,
            reservation__lt=new_time + timedelta(minutes=new_duration),
            reservation__gt=new_time - timedelta(minutes=new_duration)
        ).exclude(id=instance.id)
        if overlapping_reservations.exists():
            return Response(
                {
                    'error': 'Этот столик уже забронирован на выбранное время'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_update(serializer)
        return Response(serializer.data)
