import datetime as dt

from clickhouse_driver import Client

client = Client(host="192.168.0.118")


BATCH_SIZE = 200
MAX_ROWS = 20000


def generate_data():
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


def save_to_clickhouse(data):
    started_at = dt.datetime.now()
    for partition in data:
        client.execute(
            "INSERT INTO default.test (id, event_time) VALUES",
            (
                (
                    id_,
                    event_time,
                )
                for id_, event_time in partition
            ),
        )
    finished_at = dt.datetime.now()
    print(finished_at - started_at)


if __name__ == "__main__":
    clickhouse_data = generate_data()
    save_to_clickhouse(clickhouse_data)
