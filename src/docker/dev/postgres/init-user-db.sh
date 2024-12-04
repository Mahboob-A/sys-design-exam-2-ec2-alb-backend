#!/bin/bash
set -e

# A new user with the POSTGRES_USER will be created with the POSTGRES_PASSWORD as password for POSTGRES_DB 
psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres <<-EOSQL
    CREATE USER "$POSTGRES_USER" WITH PASSWORD "$POSTGRES_PASSWORD";
    CREATE DATABASE "$POSTGRES_DB";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
EOSQL