import datetime as dt

from clickhouse_driver import Client

# Инициализация клиента ClickHouse
clickhouse_client = Client(host="192.168.0.118")


# Параметры для генерации данных
BATCH_SIZE = 200
MAX_ROWS = 20000


def create_data_batches():
    """Генератор для создания партий данных."""
    row = BATCH_SIZE
    while row <= MAX_ROWS:
        yield [
            (
                i,
                dt.datetime.today(),
            )
            for i in range(row - BATCH_SIZE, row)
        ]
        row += BATCH_SIZE


def insert_into_clickhouse(data):
    """Сохранение данных в ClickHouse с замером времени."""
    start_time = dt.datetime.now()
    for partition in data:
        clickhouse_client.execute(
            "INSERT INTO default.test (id, event_time) VALUES",
            (
                (
                    id_,
                    event_time,
                )
                for id_, event_time in partition
            ),
        )
    end_time = dt.datetime.now()
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    clickhouse_data = create_data_batches()
    insert_into_clickhouse(clickhouse_data)
