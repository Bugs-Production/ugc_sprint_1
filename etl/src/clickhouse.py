from clickhouse_driver import Client
from config import settings


def initialize_clickhouse():
    print("initializing clickhouse")
    cl = Client(host=settings.ch_host, port=settings.ch_port)

    cl.execute(
        f"CREATE DATABASE IF NOT EXISTS {settings.ch_database} ON CLUSTER company_cluster"
    )
    cl.execute(
        f"CREATE TABLE IF NOT EXISTS {settings.ch_database}.{settings.ch_table} ON CLUSTER company_cluster "
        "(event_type String, timestamp DateTime64, user_id UUID NULL, country String, device String, "
        "element String NULL, page_url String NULL, duration Int NULL, current_time Int NULL, "
        "referrer_url Int NULL, video_id UUID NULL, from_quality Int NULL, to_quality Int NULL, "
        "filter_type String NULL, filter_value String NULL) Engine=MergeTree() ORDER BY timestamp"
    )
    print("initializing clickhouse completed")


def check_clickhouse_info():
    with Client(host=settings.ch_host, port=settings.ch_port) as cl:
        dbs = cl.execute("SHOW DATABASES")
        print("DATABASES:", dbs)
        table = cl.execute(f"SHOW TABLE {settings.ch_database}.{settings.ch_table}")
        print("TABLES:", table)

        # Пример вставки данных
        cl.execute(
            f"INSERT INTO {settings.ch_database}.{settings.ch_table} "
            "(event_type, timestamp, user_id, country, device, element, page_url) "
            "VALUES ('click', '2024-10-03T14:30:00Z', 'user123', 'US', 'mobile', 'button_submit', "
            "'https://example.com/submit')"
        )
