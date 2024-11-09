import math
import random
from random import randrange
from datetime import timedelta, datetime


def randlatlon1():
    pi = math.pi
    cf = 180.0 / pi
    gx = random.gauss(0.0, 1.0)
    gy = random.gauss(0.0, 1.0)
    gz = random.gauss(0.0, 1.0)

    norm2 = gx * gx + gy * gy + gz * gz
    norm1 = 1.0 / math.sqrt(norm2)
    x = gx * norm1
    y = gy * norm1
    z = gz * norm1

    radLat = math.asin(z)
    radLon = math.atan2(y, x)

    return round(cf * radLat, 5), round(cf * radLon, 5)


def random_date():
    delta = datetime.today() - datetime(year=2023, month=1, day=1)
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return datetime(year=2023, month=1, day=1) + timedelta(seconds=random_second)
