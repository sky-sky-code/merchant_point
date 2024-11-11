from utils import randlatlon1, random_date
import json
import random
import argparse

from db.manager import pool_manager
import logging
logging.basicConfig(level=logging.INFO)


class InitData:

    def __init__(self, pool, clients=100, merchant=300, transactions=1000):
        self.poll = pool
        self.clients = clients
        self.merchant = merchant
        self.transactions = transactions

    def generate(self):
        with self.poll as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            DO $$
                BEGIN
                    FOR i in 1..{self.clients} LOOP
                        INSERT INTO client (client_id, sex, age) VALUES (gen_random_uuid(),
                                                                         (select (array['F', 'M'])[floor(random() * 2 + 1)]),
                                                                         floor(random() * (16 - 40) + 40));
                    end loop;
            END;$$;
            """)
            logging.log(logging.INFO, "Init data client OK")

            connection.commit()
            for i in range(self.merchant):
                lat, lon = randlatlon1()
                with open('C:\\Users\\Admin\\PycharmProjects\\merchant_point\\src\\mcc_codes.json', 'r') as json_mcc:
                    mcc_cds = json.loads(json_mcc.read())
                cursor.execute(f"""
                INSERT INTO merchant_point (merchant_id, latitude, longtitude, mcc_cd) 
                VALUES (gen_random_uuid(), {lat}, {lon},{mcc_cds[random.choice([i for i in range(len(mcc_cds))])]['mcc']})""")
            logging.log(logging.INFO, "Init data merchant_point OK")
            cursor.execute('SELECT client_id FROM client')
            client_ids = cursor.fetchall()
            cursor.execute('SELECT merchant_id FROM merchant_point')
            merchant_ids = cursor.fetchall()
            for i in range(self.transactions):
                cursor.execute(f"""
                INSERT INTO transaction (uid, client_id, merchant_id, transaction_dttm, transaction_attm) VALUES (gen_random_uuid(),
                '{client_ids[random.choice([i for i in range(len(client_ids))])][0]}'::uuid, 
                '{merchant_ids[random.choice([i for i in range(len(merchant_ids))])][0]}'::uuid,
                to_timestamp('{random_date()}', 'YYYY-MM-DD hh24:mi:ss')::timestamp,{random.choice([i for i in range(1000, 10000)])})
                """)
            logging.log(logging.INFO, "Init data transaction OK")
            cursor.execute("INSERT INTO agg_table (uid) VALUES (gen_random_uuid())")
            logging.log(logging.INFO, "Init data agg_table OK")
            connection.commit()
            logging.log(logging.INFO, "Init data COMMIT ")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clients', type=int, default=100, help='Number of clients')
    parser.add_argument('-m', '--merchant', type=int, default=300, help='Number of clients')
    parser.add_argument('-t', '--transactions', type=int, default=1000, help='Number of clients')

    args = parser.parse_args()
    init_data = InitData(pool_manager, args.clients, args.merchant, args.transactions)
    init_data.generate()