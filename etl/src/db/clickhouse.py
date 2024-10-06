import logging

from clickhouse_driver import Client

from settings.config import settings

logger = logging.getLogger("etl")


def initialize_clickhouse():
    logger.info("initializing clickhouse...")
    cl = Client(host=settings.ch_host, port=settings.ch_port)

    cl.execute(
        f"CREATE DATABASE IF NOT EXISTS {settings.ch_db} ON CLUSTER company_cluster"
    )
    cl.execute(
        f"CREATE TABLE IF NOT EXISTS {settings.ch_db}.{settings.ch_table} ON CLUSTER company_cluster "
        "(event_type String, timestamp DateTime64, user_id UUID NULL, country String, device String, "
        "element String NULL, page_url String NULL, duration Int NULL, current_time Int NULL, "
        "referrer_url String NULL, video_id UUID NULL, from_quality Int NULL, to_quality Int NULL, "
        "filter_type String NULL, filter_value String NULL) Engine=MergeTree() ORDER BY timestamp"
    )
    logger.info("initializing clickhouse completed")


def check_clickhouse_info():
    with Client(host=settings.ch_host, port=settings.ch_port) as cl:
        dbs = cl.execute("SHOW DATABASES")
        logger.info(f"DATABASES: {dbs}")

        table = cl.execute(f"SHOW TABLE {settings.ch_db}.{settings.ch_table}")
        logger.info(f"TABLES: {table}")

        # Пример вставки данных
        cl.execute(
            f"INSERT INTO {settings.ch_db}.{settings.ch_table} "
            "(event_type, timestamp, user_id, country, device, element, page_url) "
            "VALUES ('click', '2024-10-03T14:30:00Z', 'user123', 'US', 'mobile', 'button_submit', "
            "'https://example.com/submit')"
        )
