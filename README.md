## О проекте

Это тестовое приложение на FastAPI с использованием PostgreSQL, Docker и pytest.

Требования

- Docker версии **4.21.1**
- Docker Compose

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/testproject1.git
cd testproject1
```

2.(Опционально) Можно изменить файл `.env` в корне проекта:

Пример `.env`:

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_NAME_TEST=postgres
```

## Запуск приложения

Чтобы запустить веб-версию приложения с пересборкой:

```bash
docker-compose --env-file .env up --build web
```

Приложение будет доступно по адресу: http://localhost:8000

## Интерфейс

**Интерфейс пользователя не реализован.**  
API доступен через Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Запуск тестов

Чтобы запустить тесты с пересборкой:

```bash
docker-compose --env-file .env run --build test
```


## Автор

- [@DimegEvs](https://github.com/DimegEvs)
