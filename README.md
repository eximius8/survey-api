# Django API для опросов

API для создания прохождения опросов. Опросы состоят из трех видов вопросов

1. Вопросы, требующие текстовый ответ
1. Вопросы, где возможно выбрать один вариант из предложенных
1. Вопросы, где можно выбрать несколько вариантов ответа

## Установка
Создаем базу (postgres) и веб сервисы
```
sudo docker-compose build
```
Готовим базу данных:
```
sudo docker-compose run web python manage.py migrate
sudo docker-compose run web python manage.py createsuperuser
```
Запускаем приложение
```
sudo docker-compose up
```
Смотрим log:
```
docker-compose logs -f web
```
## Начало работы

### Регистрация
```
curl --header "Content-Type: application/json" --request POST\
 --data '{"login":"api-user","password":"testing321"}'\
 http://127.0.0.1:8000/accounts/login/
 ```
Ответ
```
{"id":2,"username":"api-user","first_name":"","last_name":"","email":""}
```
### Вход 
```
curl --header "Content-Type: application/json" --request POST\
 --data '{"login":"api-user","password":"testing321"}'\
 http://127.0.0.1:8000/accounts/login/
```
Ответ
```
{"detail":"Login successful","token":"ced7d2f8c0720fd2ca4f44638e22ad57b5344202"}
```

## Работа администратора

### Работа с опросами
Создание опроса c тремя вопросами (пользователь администратор): 
1. Требующий текстового ответа "questiontype": "T"
1. С ответом множественного выбора "questiontype": "M"
1. С ответом единичного выбора "questiontype": "S"
```
curl -X POST  http://127.0.0.1:8000/api/surveys/\
 -H 'Authorization: Token ced7d2f8c0720fd2ca4f44638e22ad57b5344202'\
 --header "Content-Type: application/json"\
 --data '{"name":"Опрос 1","description": "Описание опроса 1", "end_date": null, 
  "questions": [
    { 
        "questiontext": "Как вы провели лето?", 
        "questiontype": "T", 
        "answers": [] 
    },
    { 
        "questiontext": "Какие ваши любимые фильмы?", 
        "questiontype": "M", 
        "answers": [
            {"option": "Иван Васильевич меняет профессию" },
            {"option": "Матрица" },
            {"option": "Шматрица" },
            {"option": "Санта Барбара" }
        ] 
    },
    { 
        "questiontext": "Какой фильм из списка является сериалом?", 
        "questiontype": "S", 
        "answers": [
            {"option": "Иван Васильевич меняет профессию" },
            {"option": "Матрица" },
            {"option": "Шматрица" },
            {"option": "Санта Барбара" }
        ] 
    }]}'
```
Ответ
```
{
    "id":21,
    "name":"Фильмы",
    "description":"Опрос посвящен фильмам",
    "start_date":"2021-01-06",
    "end_date":null,
    "questions":[
    {"id":16,
    "questiontext":"Что вы цените в кино?",
    "questiontype":"T",
    "answers":[]},
    {"id":17,
    "questiontext":"Какие ваши любимые фильмы?",
    "questiontype":"M",
    "answers":[
        {
            "id":31,"option":"Иван Васильевич меняет профессию"
            },
        {
            "id":32,"option":"Матрица"
        },
        {
            "id":33,"option":"Шматрица"
        },
        {"id":34,"option":"Санта Барбара"}
        ]},
    {"id":18,
    "questiontext":"Какой фильм из списка является сериалом?",
    "questiontype":"S",
    "answers":[
        {
            "id":35,
            "option":"Иван Васильевич меняет профессию"
        },
        {"id":36,"option":"Матрица"},
        {"id":37,"option":"Шматрица"},
        {"id":38,"option":"Санта Барбара"}]}]}
```
В случае, если пользователь не администратор
```
{"detail":"У вас недостаточно прав для выполнения данного действия."}
```
Обновление опроса (можно обновить имя, описание и дату завершения).
```
curl -X PUT http://127.0.0.1:8000/api/surveys/21/\
 -H 'Authorization: Token ced7d2f8c0720fd2ca4f44638e22ad57b5344202'\
 --header "Content-Type: application/json"\
 --data '{
    "name":"Новое имя опроса", 
    "description":"Обновленное описание", 
    "end_date":"2021-10-20"
    }'
 ```
Ответ
```
{"id":21,"name":"Новое имя опроса","description":"Обновленное описание","start_date":"2021-01-06","end_date":"2021-10-20",
"questions":[
    {"id":16,"questiontext":"Как вы провели лето?","questiontype":"T","answers":[]},
    {"id":17,"questiontext":"Какие ваши любимые фильмы?","questiontype":"M",
    "answers":[
        {"id":31,"option":"Иван Васильевич меняет профессию"},
        {"id":32,"option":"Матрица"},
        {"id":33,"option":"Шматрица"},
        {"id":34,"option":"Санта Барбара"}]},
    {"id":18,"questiontext":"Какой фильм из списка является сериалом?","questiontype":"S",
    "answers":[
        {"id":35,"option":"Иван Васильевич меняет профессию"},
        {"id":36,"option":"Матрица"},
        {"id":37,"option":"Шматрица"},
        {"id":38,"option":"Санта Барбара"}]}]}
```
### Работа с вопросами

Создание вопроса
```
curl -X POST  http://127.0.0.1:8000/api/questions/\
 -H 'Authorization: Token ced7d2f8c0720fd2ca4f44638e22ad57b5344202'\
 --header "Content-Type: application/json"\
 --data '{ 
        "questiontext": "Какой фильм из списка является сериалом?", 
        "questiontype": "S",
        "poll": 2,
        "answers": [
            {"option": "Иван Васильевич меняет профессию" },
            {"option": "Матрица" },
            {"option": "Шматрица" },
            {"option": "Санта Барбара" }
        ] 
    }'
```
Ответ {"id":19,"...
Изменение вопроса (можно изменять и удалять ответы, нельзять изменить опрос (poll) к которому привязан вопрос)
```
curl -X PUT  http://127.0.0.1:8000/api/questions/19/ \
 -H 'Authorization: Token ced7d2f8c0720fd2ca4f44638e22ad57b5344202'\
 --header "Content-Type: application/json"\
 --data '{         
        "questiontext": "Какой фильм из списка не является сериалом?", 
        "questiontype": "S",        
        "answers": [
            {"option": "Просто Мария" },
            {"option": "Матрица" },
            {"option": "Санта Барбара" }
        ] 
    }'    
```
Ответ
```
{
    "id":19,
    "questiontext":"Какой фильм из списка не является сериалом?",
    "questiontype":"S",
    "answers":[
        {"id":43,"option":"Просто Мария"},
        {"id":44,"option":"Матрица"},
        {"id":45,"option":"Санта Барбара"}],
        "poll":2
}
```

### Работа с вариантами ответов

Через /api/answers/ ответы можно только удалять и изменять но не создавать. Создание ответов происходит либо при создании опроса либо при создании или обновлении вопроса.

```
curl -X PUT http://127.0.0.1:8000/api/answers/3/\
 --header "Content-Type: application/json"\
 --data '{"option":"Измененный вариант ответа"}'
```
Удаление
```
curl -X DELETE http://127.0.0.1:8000/api/answers/13/
```

## Работа пользователя

# Что не успел

1. Тесты
1. Не написал метод update для сериалайзера опросов
1. Авторизация слишком простая через django-rest-registration без jwt и oauth
1. Возможно, более удобным было бы использование StreamField для модели вопроса