### API для проекта Yamdb.
Возможности:
- создание произведений, отзывов, категорий, жанров.
- JWT-аунтефикация по коду подтверждения через email
- комментирование отзывов

Для начала работы требуется клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/oupsfed/api_yamdb.git
```

```
cd api_final_yamdb
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
GET api/v1/titles
```

```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```

Для подробной информации посетите /redoc/
