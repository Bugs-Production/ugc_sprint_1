from clickhouse_driver import Client
from config import settings


def initialize_clickhouse():
    print("initializing clickhouse")
    cl = Client(host=settings.ch_host, port=settings.ch_port)

    cl.execute(
        f"CREATE DATABASE IF NOT EXISTS {settings.ch_database} ON CLUSTER company_cluster"
    )
    cl.execute(
        f"CREATE TABLE IF NOT EXISTS {settings.ch_database}.{settings.ch_table} ON CLUSTER company_cluster (type String, "
        f"timestamp DateTime64, user_id UUID NULL, fingerprint String, element String NULL, url String NULL, "
        f"time Int NULL, id_film UUID NULL, film String NULL, original_quality Int NULL, updated_quality Int NULL, "
        f"filter String NULL) Engine=MergeTree() ORDER BY timestamp"
    )
    print("initializing clickhouse completed")


def check_clickhouse_info():
    with Client(host=settings.ch_host, port=settings.ch_port) as cl:
        dbs = cl.execute("SHOW DATABASES")
        print("DATABASES:", dbs)
        table = cl.execute(f"SHOW TABLE {settings.ch_database}.{settings.ch_table}")
        print("TABLES:", table)
