# Phone Info Service

Сервис определения оператора и региона мобильного номера с интеграцией Voxlink API

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Основные возможности

✔ Определение оператора связи по номеру телефона  
✔ Показ региона (город/область)  
✔ История предыдущих запросов  
✔ Админ-панель для управления данными  
✔ Адаптивный веб-интерфейс  
✔ REST API для интеграций  

## 🛠 Технологический стек

**Backend**:

- Django 5.0
- Python 3.11+
- Django REST Framework

**База данных**:

- PostgreSQL

**Кэширование**:

- Redis (планируется)

**Frontend**:

- Bootstrap 5 (планируется)
- HTML5 + CSS3

## 🚀 Установка и запуск

### Требования

- Python 3.11+
- PostgreSQL 15+
- Redis 6+
- Poetry 1.6+

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-username/phone_info_service.git
cd phone_info_service
```

### 2. Настройка окружения

**Создайте файл .env на основе примера:**

```bash
cp .env.example .env
```

**Отредактируйте параметры в .env:**

```ini
DB_NAME=phone_info
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=True
REDIS_URL=redis://localhost:6379/0
PHONE_API_URL=https://num.voxlink.ru/get/
```

### 3. Установка зависимостей

```bash
poetry install
```

### 4. Настройка базы данных

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
poetry run python manage.py runserver
```

**Сервис будет доступен по адресу: <http://localhost:8000>**

## 📚 Документация API

Проверка номера

```http
GET /api/check/?phone=79991234567
```

**Пример ответа:**

```json
{
  "number": "+79991234567",
  "operator": "МТС",
  "region": "Москва",
  "is_new": false,
  "first_query": "2025-07-08T12:00:00Z"
}
```

История запросов

```http
GET /api/history/
```

## 📜 Лицензия

**Проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.**
