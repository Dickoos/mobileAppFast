"""
ЭТО ТЕСТОВЫЙ ФАЙЛ
Просто проверка работоспособности
Сейчас такой таблицы в базе данных НЕТ!
"""


import psycopg2

from psycopg2.extensions import connection, cursor


def get_connection_and_cursor(dbname: str, user: str, password: str, host: str) -> (connection, cursor):
    """
    Allows you to get the database connection and cursor.

    :param dbname: Database name.
    :param user: Username.
    :param password: User password.
    :param host: Server ip with db.
    :return: Database connection and cursor that allows making database queries.
    """

    temp_connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    temp_cursor = temp_connection.cursor()

    return temp_connection, temp_cursor


def get_people_from_db(temp_cursor: cursor) -> list:
    """
    Gets a list of ALL people in the database.

    :param temp_cursor: Database cursor.
    :return: List of all people.
    """

    query = """
    SELECT
        *
    FROM
        people
    """

    temp_cursor.execute(query)

    return temp_cursor.fetchall()


def add_person_to_db(temp_connection: connection, temp_cursor: cursor, name: str, company: str) -> None:
    """
    Adds a person to the database.

    :param temp_connection: Connection to the database.
    :param temp_cursor: Database cursor.
    :param name: Name of person.
    :param company: Name of company in which person works.
    :return: None.
    """

    query = """
    INSERT INTO
        people
    VALUES
        (%s, %s)
    """
    values = (name, company)

    temp_cursor.execute(query, values)
    temp_connection.commit()


if __name__ == '__main__':
    main_connection, main_cursor = get_connection_and_cursor("test", "pi", "23514317", "192.168.1.69")

    add_person_to_db(main_connection, main_cursor, "test name", "test company")

    for people in get_people_from_db(main_cursor):
        print(people)

    main_cursor.close()
    main_connection.close()
