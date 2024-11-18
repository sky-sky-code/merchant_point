#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE merchant_point;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "merchant_point" <<-EOSQL
CREATE DOMAIN public.gender AS character(1)
	CONSTRAINT gender_check CHECK ((VALUE = ANY (ARRAY['F'::bpchar, 'M'::bpchar])));

  CREATE TABLE IF NOT EXISTS client(
    client_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sex gender,
    age smallint
);

EOSQL
