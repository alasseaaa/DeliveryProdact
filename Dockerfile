# Основа образа - Python 3.10.6
FROM python:3.10.6

RUN python -m pip install --upgrade pip
WORKDIR /app
# Установка необходимых пакетов
COPY requirements.txt .
RUN pip install -r requirements.txt


# Копирование файлов проекта в контейнер
COPY . .

# Установка зависимостей Django
# RUN python manage.py migrate

# Запуск Django сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]