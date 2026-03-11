# Домашнее задание к занятию "`Asyncio`" - `Дёмин Максим`


### Задание 1

Что нужно сделать:

В этом задании мы будем выгружать из API персонажей Start Wars и загружать в базу данных.

Документация по API находится здесь: SWAPI.

Пример запроса: https://www.swapi.tech/api/people/1/

В результате запроса получаем персонажа с ID 1:

```
{
  "message": "ok",
  "result": {
    "properties": {
      "created": "2025-07-22T16:28:46.488Z",
      "edited": "2025-07-22T16:28:46.488Z",
      "name": "Luke Skywalker",
      "gender": "male",
      "skin_color": "fair",
      "hair_color": "blond",
      "height": "172",
      "eye_color": "blue",
      "mass": "77",
      "homeworld": "https://www.swapi.tech/api/planets/1",
      "birth_year": "19BBY",
      "url": "https://www.swapi.tech/api/people/1"
    },
    "_id": "5f63a36eee9fd7000499be42",
    "description": "A person within the Star Wars universe",
    "uid": "1",
    "__v": 2
  },
  "apiVersion": "1.0",
  "timestamp": "2025-07-22T19:39:54.218Z",
  "support": {
...
  },
  "social": {
...
  }
}
```

Необходимо выгрузить cледующие поля:
id - ID персонажа
birth_year
eye_color
gender
hair_color
homeworld
mass
name
skin_color
Данные по каждому персонажу необходимо загрузить в любую базу данных.
Выгрузка из апи и загрузка в базу должна происходить асинхронно.

Результатом работы будет:

скрипт миграции базы данных
скрипт загрузки данных из API в базу
В базу должны быть загружены все персонажи

Решение:

Подготовка базы 
Создать базу данных и применить миграцию: 
psql -U postgres -d starwars -f create_people.sql

Установка зависимостей 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Запуск загрузки 
export DATABASE_DSN='postgresql://postgres:postgres@localhost:5432/starwars'
python load_people.py

Проверка 
psql -U postgres -d starwars -c "SELECT COUNT(*) FROM people;"
psql -U postgres -d starwars -c "SELECT id, name, gender, birth_year FROM people ORDER BY id LIMIT 10;"
