from db.manager import PoolManager
from controller import Controller
from routing import App

pool = PoolManager(
    1, 2,
    user='dev',
    password='dev',
    host='127.0.0.1',
    port='5432',
    database='merchant_point'
)

app = App()


def generate_filter_sql(**kwargs):
    sql_filter = []
    if kwargs['sex'] is not None:
        sql_filter.append(f"client.sex = '{kwargs["sex"]}'")
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


@app.route('sum')
def sum_transaction(**kwargs):
    aggregate_name_column = []
    for key in kwargs.keys():
        if kwargs[key] is not None:
            aggregate_name_column.append(f'{key}_{kwargs[key]}')
    aggregate_name_column = '_'.join(aggregate_name_column)
    sql_filter = "where " + generate_filter_sql(**kwargs) if generate_filter_sql(**kwargs) != '' else ""
    with pool as connection:
        cursor = connection.cursor()
        cursor.execute(f"""select column_name from information_schema.columns 
                           where table_name = 'agg_table' and column_name = '{aggregate_name_column.lower()}'""")
        exists_column_agg = cursor.fetchall()
        if not exists_column_agg:
            cursor.execute(f"ALTER TABLE agg_table ADD COLUMN {aggregate_name_column} INT NULL")

        cursor.execute(f"""select SUM(transaction_attm)  from transaction
                           JOIN client on transaction.client_id = client.client_id JOIN
                           merchant_point ON transaction.merchant_id = merchant_point.merchant_id {sql_filter}""")
        agg_data = cursor.fetchall()
        if agg_data[0][0]:
            cursor.execute("SELECT uid FROM agg_table")
            check_not_empty_table = cursor.fetchall()
            if not check_not_empty_table:
                cursor.execute(f"INSERT INTO agg_table ({aggregate_name_column}) VALUES ({agg_data[0][0]})")
            else:
                cursor.execute(
                    f"UPDATE agg_table SET {aggregate_name_column} = {agg_data[0][0]} WHERE uid = '{check_not_empty_table[0][0]}'")
        connection.commit()


@app.route('agg')
def agg_transaction(**kwargs):
    pass


@app.route('count')
def count_transaction(**kwargs):
    pass


if __name__ == '__main__':
    cont = Controller(app)
    cont()
