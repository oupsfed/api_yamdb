### API для проекта Yatube.
Возможности:
- создание постов, комментариев
- JWT-аунтефикация
- Получения данных либо всех, либо конктреных объектов (постов, групп, комментариев)
- Подписки на авторов, а так же просмотр своих подписок

Для начала работы требуется клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/oupsfed/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Примеры работы API:
```
GET api/v1/posts
```

```
{
"count": 123,
"next": "http://api.example.org/accounts/?offset=400&limit=100",
"previous": "http://api.example.org/accounts/?offset=200&limit=100",
"results": [
{}
]
}
```

Для подробной информации посетите /redoc/
