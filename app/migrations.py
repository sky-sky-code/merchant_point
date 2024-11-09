from db.manager import pool_manager

with pool_manager as connection:
    cursor = connection.cursor()
    cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (select * from pg_type where typname = 'gender') THEN
                        CREATE DOMAIN gender CHAR(1)
                            check ( value IN ('F', 'M'));
                END IF;
            END$$;
            
            CREATE TABLE IF NOT EXISTS merchant_point(
                merchant_id uuid PRIMARY KEY  DEFAULT gen_random_uuid(),
                latitude DECIMAL(8, 6),
                longtitude DECIMAL(9, 6),
                mcc_cd integer
            );
            
            
            CREATE TABLE IF NOT EXISTS client(
                client_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                sex gender,
                age smallint
            );
            
            Create table IF NOT EXISTS transaction(
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                merchant_id UUID REFERENCES merchant_point(merchant_id),
                client_id UUID REFERENCES client(client_id),
                transaction_dttm timestamp,
                transaction_attm integer
            );
            Create table IF NOT EXISTS agg_table(
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid()
            );
        """)
    connection.commit()
