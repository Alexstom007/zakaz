# Restaurant Table Reservation API

REST API для бронирования столиков в ресторане.

## Функциональность

- Создание, просмотр и удаление столиков
- Создание, просмотр и удаление броней
- Проверка на пересечение броней по времени
- Валидация данных на уровне API

## Технологии

- Django
- Django REST Framework
- PostgreSQL
- Docker
- pytest

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd stol
```

2. Установите переменные окружения:
   - `DB_ENGINE`: движок базы данных (по умолчанию `django.db.backends.postgresql`)
   - `POSTGRES_DB`: имя базы данных (по умолчанию `zakaz_db`)
   - `POSTGRES_USER`: пользователь базы данных (по умолчанию `user`)
   - `POSTGRES_PASSWORD`: пароль пользователя базы данных
   - `DATABASE_HOST`: хост базы данных (по умолчанию `db`)
   - `DB_PORT`: порт базы данных (по умолчанию `5432`)

3. Запустите приложение с помощью Docker Compose:
```bash
docker-compose up --build
```

4. После запуска контейнеров выполните миграции базы данных:
```bash
docker-compose exec web python manage.py migrate
```

5. Приложение будет доступно по адресу: http://localhost:8000

## API Endpoints

### Столики
- GET /api/tables/ - список всех столиков
- POST /api/tables/ - создать новый столик
- GET /api/tables/{id}/ - получить информацию о конкретном столике
- PUT /api/tables/{id}/ - обновить информацию о столике
- DELETE /api/tables/{id}/ - удалить столик


#### Пример JSON-запроса на создание столика:
```json
{
  "name": "Столик 1",
  "seats": 4,
  "location": "У окна"
}
```

### Брони
- GET /api/reservations/ - список всех броней
- POST /api/reservations/ - создать новую бронь
- GET /api/reservations/{id}/ - получить информацию о конкретной брони
- PUT /api/reservations/{id}/ - обновить информацию о брони
- DELETE /api/reservations/{id}/ - удалить бронь


#### Пример JSON-запроса на создание брони:
```json
{
  "customer": "Иван",
  "table": 1,
  "reservation": "2025-10-10T18:00:00Z",
  "duration": 60
}
```
Александр Вотинов- [https://github.com/Alexstom007]