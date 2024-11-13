from psycopg2 import pool
from merchant.settings import POSTGRES_HOST, POSTGRES_USER, POSTGRES_DATABASE, POSTGRES_PASSWORD, POSTGRES_PORT


class PoolManager:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._pool: pool.SimpleConnectionPool = None
        self._connection = None

    def __enter__(self):
        if self._pool is None:
            self._pool = pool.SimpleConnectionPool(*self.args, **self.kwargs)

        self._connection = self._pool.getconn()
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._pool.putconn(self._connection)
        self._pool.closeall()
        self._connection = None


pool_manager = PoolManager(
    1, 2,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DATABASE
)
