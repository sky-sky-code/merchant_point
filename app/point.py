from db.manager import pool_manager
import argparse
import logging

logging.basicConfig(level=logging.INFO)


def generate_filter_sql(**kwargs):
    sql_filter = []
    if kwargs['sex'] is not None:
        sql_filter.append(f"""client.sex = '{kwargs["sex"]}'""")
    if kwargs['age'] is not None:
        if "-" in kwargs['age']:
            age = kwargs["age"].split("-")
            sql_filter.append(f'client.age <= {age[0]} <= client.age {age[1]}')
        elif int(kwargs['age']) >= 31:
            sql_filter.append(f'client.age >= {kwargs["age"]}')
        else:
            sql_filter.append(f'client.age <= {kwargs["age"]}')
    if kwargs['year'] is not None:
        sql_filter.append(f'extract(year FROM transaction_dttm) = {kwargs["year"]}')
    if kwargs['month'] is not None:
        sql_filter.append(f'extract(month FROM transaction_dttm) = {kwargs["month"]}')
    if kwargs['mcc'] is not None:
        sql_filter.append(f'merchant_point.mcc_cd = {kwargs["mcc"]}')
    return ' and '.join(sql_filter)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('agg')
    parser.add_argument('-s', "--sex", help='Введите пол')
    parser.add_argument('-a', "--age", help='Введите возраст')
    parser.add_argument('-y', "--year", help='Введите год')
    parser.add_argument('-m', "--month", help='Введите месяц')
    parser.add_argument('-mc', "--mcc", help='Введите mcc код')

    parse_args = parser.parse_args()
    arguments = {
        'agg': parse_args.agg,
        'sex': parse_args.sex,
        'age': parse_args.age,
        'year': parse_args.year,
        'month': parse_args.month,
        'mcc': parse_args.mcc
    }
    logging.log(logging.INFO,
       f"Функция аггрeгации: {arguments['agg']} | Фальтрация: "
       f"{ ' '.join([f'{key}={arguments[key]}' for key in arguments.keys() if key != 'agg' and arguments[key] != None]) }"
    )
    aggregate_name_column = []
    for key in arguments.keys():
        if arguments[key] is not None:
            aggregate_name_column.append(f'{key}_{arguments[key]}')
    aggregate_name_column = '_'.join(aggregate_name_column)
    sql_filter = "where " + generate_filter_sql(**arguments) if generate_filter_sql(**arguments) != '' else ""

    with pool_manager as connection:
        cursor = connection.cursor()
        cursor.execute(f"""select column_name from information_schema.columns 
                           where table_name = 'agg_table' and column_name = '{aggregate_name_column.lower()}'""")

        exists_column_agg = cursor.fetchall()
        if not exists_column_agg:
            cursor.execute(f"ALTER TABLE agg_table ADD COLUMN {aggregate_name_column} INT NULL")
            logging.log(logging.INFO, f"Создание столбца {aggregate_name_column} c значением null")

        cursor.execute(f"""select {parse_args.agg}(transaction_attm)  from transaction
                           JOIN client on transaction.client_id = client.client_id JOIN
                           merchant_point ON transaction.merchant_id = merchant_point.merchant_id {sql_filter}""")
        agg_data = cursor.fetchall()
        logging.log(logging.INFO, f"Обработка данных")
        if agg_data[0][0]:
            cursor.execute("SELECT uid FROM agg_table LIMIT 1")
            uid_agg = cursor.fetchall()
            cursor.execute(
                f"UPDATE agg_table SET {aggregate_name_column} = {agg_data[0][0]} WHERE uid = '{uid_agg[0][0]}'")
            logging.log(logging.INFO, f"Вставка данных {agg_data[0][0]} в поле {aggregate_name_column}")
        connection.commit()
