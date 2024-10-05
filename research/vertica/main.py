import csv
import datetime

import vertica_python
from timer import timer

# Параметры для подключения к базе данных Vertica
db_config = {
    "host": "127.0.0.1",
    "port": 5433,
    "user": "dbadmin",
    "password": "",
    "database": "docker",
    "autocommit": True,
}


@timer
def bulk_insert(data):
    """Функция для вставки данных в таблицу netflix_titles."""
    count = 0
    while count <= 10000000:

        for each in data:
            cursor.execute(
                f"""INSERT INTO netflix_titles(type, title, director, cast_title, country, date_added, release_year, 
                rating, duration) VALUES ('{each[0]}', '{each[1]}', '{each[2]}', '{each[3]}', '{each[4]}',
                '{each[5]}', '{each[6]}', '{each[7]}', '{each[8]}')"""
            )
            count += 1

        return


@timer
def fetch_all_data():
    """Функция для выборки всех данных из таблицы netflix_titles."""
    cursor.execute(
        """
            SELECT * FROM netflix_titles;
        """
    )
    for row in cursor.iterate():
        print(row)


with vertica_python.connect(**db_config) as connection:  # 1
    cursor = connection.cursor()  # 2
    cursor.execute(
        """  
        DROP TABLE if exists netflix_titles 
        """
    )
    cursor.execute(
        """  
    CREATE TABLE if not exists netflix_titles (
        id IDENTITY,
        type VARCHAR(256) NOT NULL,
        title VARCHAR(1024) NOT NULL,
        director VARCHAR(1024) DEFAULT NULL,
        cast_title VARCHAR(1024) DEFAULT NULL,
        country VARCHAR(1024) NOT NULL,
        date_added DATE DEFAULT NULL,
        release_year DATE DEFAULT NULL,
        rating VARCHAR(256) NOT NULL,
        duration VARCHAR(256) NOT NULL
    );
    """
    )

    with open("netflix_titles.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile)
        spamreader.__next__()
        data = []
        format = "%B %d, %Y"
        for row in spamreader:
            date_added = (
                datetime.datetime.strptime(row[6].strip(), format)
                if row[6]
                else datetime.date.today()
            )
            if date_added:
                date_added = f"{date_added.year}-{date_added.month}-{date_added.day}"
            title = (
                row[1],
                row[2].replace("'", ""),
                row[3].replace("'", ""),
                row[4].replace("'", ""),
                row[5],
                date_added,
                f"{row[7]}-1-1",
                row[8],
                row[9],
            )
            data.append(title)

    bulk_insert(data)
    fetch_all_data()
