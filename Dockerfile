# Використовуємо офіційний образ Python
FROM python:3.10-slim

# Встановлюємо необхідні бібліотеки
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копіюємо код бота в середину контейнера
COPY src /app

# Робочий каталог
WORKDIR /app

# Команда для запуску бота
CMD ["sh", "-c", "python main.py"]
