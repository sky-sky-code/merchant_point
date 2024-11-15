# Merchant

# DataBase

Создайте базу данных __merchant_point__


чтобы функции агригации работали нужно запустить миграцию и генерацию данных <br>
файлы __migrations.py__  и __init_data.py__<b>

## Миграции

```
python -m merchant.app.migrations
```
Соаздает 4 Таблицы

Table merchant_point <br>
- merchant_id
- latitube
- longtitube
- mcc_cd

Table client
- client_id
- sex
- age

Table transaction
- uid
- merchant_id
- client_id
- transaction_dttm
- transaction_attm

Table agg_table
- uid
- dynamic column agg


## Генерация данных

    python -m merchant.app.init_data

Запускает генерацию данных для таблиц clients, merchant_point, transaction, agg_table <br>
Необязательные аргументы:
- -с указывается количество клиентов. По умолчанию 100
- -m указывается количество торговых точек. По умолчанию 300
- -t указывается количество транзакций. По умолчанию 1000

# Аггрегация

    python -m merchant.app.point [sum,avg, count] -s -a -y -m -mc

Применение функций агригации и сохраненние результата в таблицу agg_table <br>
Обязательные аргументы:
- agg: определение функций агрегации sum, avg, count

<br>
Необязательные аргументы:

- -s: пол[F, M]
- -a: возраст
- -y: год
- -m: месяц
- -mc: код торговой точки

## Dump

Для проверки данных dump находится ./merchant/src/dump.sql
***

# ETL

1. Поднять сервисы

        docker-compose up

2. перейти в nifi http://localhost:8080
3. загрузить в nifi конфигурацию .src/template2.xml

# MINIO
Настройка базы
1. Создайте базу merchant_point по localhost:5433
2. Создайте таблицу client пример DDL в migrations.py


Настройка minio
1. загрузите клиент minio https://min.io/docs/minio/windows/index.html
2. выолните комманды minio client


    mc mb local/source

    mc admin config set local notify_webhook:nifi endpoint=http://nifi:8086
    
    mc admin service restart local
    
    mc event add local/source arn:minio:sqs::nifi:webhook --event put

Загрузка файлов

1. Зайдите в minio http:/127.0.0.1:9001
2. перейдите в bucket source
3. Загрузите файл .src/clients.csv


