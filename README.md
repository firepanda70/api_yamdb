# Описание

API для системы хранения отзывов
к произведениям культуры

# Установка

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/firepanda70/api_yamdb
cd api_yamdb
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

- Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python3 manage.py migrate
```

- Запустить проект:

```
python3 manage.py runserver
```

# Авторы
[thelie](https://github.com/thelie) - управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail, поля.

[IPfa](https://github.com/IPfa) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них.

[firepanda70](https://github.com/firepanda70) - отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений.

# Лицензия
MIT License
