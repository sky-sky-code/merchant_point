from utils import randlatlon1, random_date
import json
import random


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
            connection.commit()
            for i in range(self.merchant):
                lat, lon = randlatlon1()
                with open('C:\\Users\\Admin\\PycharmProjects\\merchant_point\\src\\mcc_codes.json', 'r') as json_mcc:
                    mcc_cds = json.loads(json_mcc.read())
                cursor.execute(f"""
                INSERT INTO merchant_point (merchant_id, latitude, longtitude, mcc_cd) 
                VALUES (gen_random_uuid(), {lat}, {lon},{mcc_cds[random.choice([i for i in range(len(mcc_cds))])]['mcc']})""")
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
            connection.commit()
