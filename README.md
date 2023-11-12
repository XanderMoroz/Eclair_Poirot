## Инструкция по установке
1. ### Подготовка проекта

1.1 Клонируете репозиторий
```sh
git clone https://github.com/XanderMoroz/Eclair_Poirot.git
```

1.2 В корневой папки клонированного репозитория создаете файл .env

1.3 В файлe .env создаете переменные для подключеня к базе данных. Например:

```sh
# Project settings
SECRET_KEY=DVnFmhwvjEhJZpuhndxjhlezxQPJmBIIkMDEmFREWQADPcUnrG
ENVIRONMENT=DEV
# Postgres settings
DEFAULT_DB_HOST=postgres
DEFAULT_DB_USER=postgres
DEFAULT_DB_PASS=postgres
DEFAULT_DB_PORT=5432
DEFAULT_DB_NAME=app_db
```
2. ### Запуск проекта с Doker

2.1 Создаете и запускаете контейнер через терминал:
```sh
sudo docker-compose up --build
```
2.2 Сервис доступен по адресу: http://0.0.0.0:8000/ 
Админка доступна по адресу: http://0.0.0.0:8000/admin