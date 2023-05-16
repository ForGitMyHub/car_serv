# Откуда берём образ
FROM python:3.11

# Создаём рабочую папку внутри контейнера
RUN mkdir /carservice_doc

# Назначаем рабочую папку
WORKDIR /carservice_doc

# Для начала переносим файл с зависимостями в нашу рабочую папку (Также он кэшируется и если файл не обновится, то время не будет тратиться
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь проект рабочую папку (Если что-то изменится - автоматом перенесутся изменения)
COPY . .


# Команда на доступ к bash скриптам из этой папки
RUN chmod a+x /carservice_doc/docker/*.sh


# Исполняется весь код до CMD
# в продакшене не используется reload (А вместо uvicorn - gunicorn)
CMD ["gunicorn", "src.main:app","--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
# Указываем количество воркеров (минимум 1), далее указываем класс воркера и связываем порт

