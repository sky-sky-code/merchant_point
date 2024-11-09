from db.manager import PoolManager

pool = PoolManager(
    1, 2,
    user='dev',
    password='dev',
    host='127.0.0.1',
    port='5432',
    database='merchant_point'
)
