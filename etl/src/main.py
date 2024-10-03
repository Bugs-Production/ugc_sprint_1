from clickhouse import check_clickhouse_info, initialize_clickhouse


def main():
    print("Initializing, create DB, Table...")
    initialize_clickhouse()

    # TODO: to delete after full setup
    print("Check DB, Tables")
    check_clickhouse_info()


if __name__ == "__main__":
    main()
