FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


WORKDIR /opt/app


RUN apt update && apt install -y --no-install-recommends \
    gcc libpq-dev curl netcat \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r web \
    && useradd -d /opt/app -r -g web web

COPY ./requirements.txt .


RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


COPY --chown=web:web . .


RUN chmod +x app.sh


ENTRYPOINT ["/opt/app/app.sh"]