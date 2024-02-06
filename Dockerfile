# Используем официальный образ Python
FROM python:3.8

# Устанавливаем переменную окружения для отключения вывода логов Python в буферизированный режим
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в рабочую директорию
COPY requirements.txt /app/
COPY config.py /app/
COPY db_connector.py /app/
COPY slack_notifier.py /app/
COPY main.py /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем ваш скрипт main.py в фоновом режиме
CMD ["python", "main.py", "&"]