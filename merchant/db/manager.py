from psycopg2 import pool


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
    user='dev',
    password='dev',
    host='127.0.0.1',
    port='5432',
    database='merchant_point'
)
