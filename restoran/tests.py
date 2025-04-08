import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

from .models import Table, Reservation


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def table():
    return Table.objects.create(
        name='Тестовый столик',
        seats=4,
        location='У окна'
    )


@pytest.mark.django_db
class TestTableModel:
    def test_table_creation(self):
        """Тест создания столика"""
        table = Table.objects.create(
            name='Столик 1',
            seats=4,
            location='У окна'
        )
        assert table.name == 'Столик 1'
        assert table.seats == 4
        assert table.location == 'У окна'
        assert str(table) == 'Столик 1 (4 мест) - У окна'


@pytest.mark.django_db
class TestReservationModel:
    def test_reservation_creation(self, table):
        """Тест создания бронирования"""
        reservation = Reservation.objects.create(
            customer='Тестовый клиент',
            table=table,
            reservation=timezone.now() + timedelta(days=1),
            duration=60
        )
        assert reservation.customer == 'Тестовый клиент'
        assert reservation.table == table
        assert reservation.duration == 60

    def test_reservation_validation(self, table):
        """Тест валидации пересечения бронирований"""
        Reservation.objects.create(
            customer='Клиент 1',
            table=table,
            reservation=timezone.now() + timedelta(days=1),
            duration=60
        )
        with pytest.raises(Exception):
            Reservation.objects.create(
                customer='Клиент 2',
                table=table,
                reservation=timezone.now() + timedelta(days=1),
                duration=60
            )


@pytest.mark.django_db
class TestTableAPI:
    def test_get_tables(self, client, table):
        """Тест получения списка столиков через API"""
        url = reverse('table-list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Тестовый столик'

    def test_create_table(self, client):
        """Тест создания нового столика через API"""
        url = reverse('table-list')
        data = {
            'name': 'Новый столик',
            'seats': 4,
            'location': 'У стены'
        }
        response = client.post(url, data)
        assert response.status_code == 201
        assert response.data['name'] == 'Новый столик'


@pytest.mark.django_db
class TestReservationAPI:
    def test_get_reservations(self, client, table):
        """Тест получения списка бронирований через API"""
        Reservation.objects.create(
            customer='Тестовый клиент',
            table=table,
            reservation=timezone.now() + timedelta(days=1),
            duration=60
        )
        url = reverse('reservation-list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['customer'] == 'Тестовый клиент'

    def test_create_reservation(self, client, table):
        """Тест создания нового бронирования через API"""
        url = reverse('reservation-list')
        data = {
            'customer': 'Новый клиент',
            'table': table.id,
            'reservation': (timezone.now() + timedelta(days=1)).isoformat(),
            'duration': 60
        }
        response = client.post(url, data)
        assert response.status_code == 201
        assert response.data['customer'] == 'Новый клиент'

    def test_create_invalid_reservation(self, client, table):
        """Тест создания бронирования с прошедшей датой через API"""
        url = reverse('reservation-list')
        data = {
            'customer': 'Новый клиент',
            'table': table.id,
            'reservation': (timezone.now() - timedelta(days=1)).isoformat(),
            'duration': 60
        }
        response = client.post(url, data)
        assert response.status_code == 400
