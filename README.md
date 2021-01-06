# Django API для опросов

API для создания прохождения опросов. Опросы состоят из трех видов вопросов

1. Вопросы, требующие текстовый ответ
1. Вопросы, где возможно выбрать один вариант из предложенных
1. Вопросы, где можно выбрать несколько вариантов ответа

## Установка
Создаем базу (postgres) и веб сервисы
```
docker-compose build
```
Готовим базу данных:
```
sudo docker-compose run web python manage.py migrate
sudo docker-compose run web python manage.py createsuperuser
```
Запускаем приложение
```
docker-compose up
```
Смотрим log:
```
docker-compose logs -f web
```

## Создание опросов

Опрос без вопросов 
```
curl --header "Content-Type: application/json" --request POST\
 --data '{"name":"Опрос 1","description": "Описание опроса 1", "end_date": null, "questions": []}'\
 http://127.0.0.1:8000/api/surveys/
```

## Работа с вариантами ответов

### Изменение ответа

```
curl -X PUT http://127.0.0.1:8000/api/answers/3/\
 --header "Content-Type: application/json"\
 --data '{"option":"Измененный вариант ответа"}'
```

### Удаление ответа

```
curl -X DELETE http://127.0.0.1:8000/api/answers/13/
```