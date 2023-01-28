FROM python:3.10

WORKDIR /app-store

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["/bin/bash", "docker-entrypoint.sh"]
