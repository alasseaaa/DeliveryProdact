FROM python:3.13
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && apt install -y postgresql-client

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt;

COPY . .

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]