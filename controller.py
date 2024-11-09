import argparse


class Controller:

    def __init__(self, app):
        parser = argparse.ArgumentParser()
        parser.add_argument('point')
        parser.add_argument('-s', "--sex", help='Введите пол')
        parser.add_argument('-a', "--age", help='Введите возраст')
        parser.add_argument('-y', "--year", help='Введите год')
        parser.add_argument('-m', "--month", help='Введите месяц')
        parser.add_argument('-mc', "--mcc", help='Введите mcc код')

        self.parse_args = parser.parse_args()
        self.app = app

    def __call__(self, *args, **kwargs):
        self.app(agg=self.parse_args.point,
                 sex=self.parse_args.sex,
                 age=self.parse_args.age,
                 year=self.parse_args.year,
                 month=self.parse_args.month,
                 mcc=self.parse_args.mcc)
