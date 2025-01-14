FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=web:web . .

RUN chmod +x app.sh

# Команда для вывода содержимого директории; не обязательно
RUN echo "Содержимое директории /opt/app:" && ls -la /opt/app

# Точка входа, но она не будет автоматически выполняться, когда вы будете просматривать образ
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=web:web . .

RUN chmod +x app.sh

# Команда для вывода содержимого директории; не обязательно
RUN echo "Содержимое директории /opt/app:" && ls -la /opt/app

# Используем команду-заглушку для удержания контейнера
CMD ["tail", "-f", "/dev/null"]
