# Проект Wallet

## Описание
Wallet - это проект, представляющий собой веб-приложение для управления финансами, которое позволяет пользователям создавать, пополнять и отслеживать свои кошельки. Проект написан на Python с использованием FastAPI, SQLAlchemy и Alembic для управления базой данных (Postgres).

## Установка и запуск проекта
1. Создайте в директории src файл .env
2. Заполните переменные
Пример:
```commandline
#APP
TITLE=Wallet API

#DB
POSTGRES_USER=postgresuser
POSTGRES_PASSWORD=postgrespassword
POSTGRES_DB=postgresdb
POSTGRES_PORT=5432
POSTGRES_HOST=postgreshost

#JWT
SECRET_KEY=0d26a88b48fc428ba846d161ffe3da45
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

#WEBHOOK
WEBHOOK_SECRET_KEY=gfdmhghif38yrf9ew0jkf32
```
3. Находясь в корне проекта запустите композ файл командой
```commandline
docker compose -f docker/docker-compose.yml up --build
```
4. Swagger будет доступен на ```http://127.0.0.1:8000/docs```
5. Для тестирования созданы:
- Тестовый пользователь:
```commandline
{
  "email": "testuser@example.com",
  "password": "159753456"
}
```
- Тестовый администратор:
```commandline
{
  "email": "admin@example.com",
  "password": "testpass"
}
```
- Тестовый счет пользователя 