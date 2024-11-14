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

Применение функций агригации и сохраненние результата в базу agg_table <br>
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




