# Analyzer Service

## Описание
Analyzer Service — это проект, предоставляющий API на базе FastAPI с документацией Swagger. Использует PostgreSQL в качестве базы данных и Docker для удобного развёртывания.

### Требования
- Docker
- Docker Compose

### Установка и запуск

1. Склонируйте репозиторий:
    ```
    https://github.com/axem4n31/Analyzer-Service.git
    cd Analyzer-Service
    ```
2. Создайте файл .env и скопируйте туда данные из файла .env.template:

3. Запустите приложение с помощью Docker::
    ```
    docker-compose up --build
    ```
4. После успешного развёртывания перейдите по адресу http://localhost:8080/docs для доступа к Swagger UI.

### Использование
- Для взаимодействия с API используйте Swagger UI по адресу http://localhost:8080/docs, где вы сможете тестировать все доступные эндпоинты.

### Остановка
Для остановки приложения используйте:
```
docker-compose down
```

### Примечания
- Убедитесь, что порты 8080 (для FastAPI) и 5432 (для PostgreSQL) не заняты другими приложениями на вашем компьютере.
- Для изменения порта доступа к приложению, отредактируйте файл docker-compose.yml и укажите другой порт в секции ports.

### Контакты
- Автор: Топоров Денис
- Email: toporov.axeman@gmail.com
- Telegram: @axem4n