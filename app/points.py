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


@app.route('sum')
def sum_transaction(**kwargs):
    pass


@app.route('agg')
def agg_transaction(**kwargs):
    pass


@app.route('count')
def count_transaction(**kwargs):
    pass


if __name__ == '__main__':
    cont = Controller(app)
    cont()
