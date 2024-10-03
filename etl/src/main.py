import logging

from clickhouse import check_clickhouse_info, initialize_clickhouse
from logger import setup_logger

logger = logging.getLogger("etl")


def main():
    initialize_clickhouse()

    # TODO: to delete after full setup
    check_clickhouse_info()


if __name__ == "__main__":
    setup_logger()
    main()
