import psycopg2

from psycopg2.extensions import connection, cursor


class DB:
    dbname = str()
    user = str()
    password = str()
    host = str()
    connection = None
    cursor = None

    user_table_name = str()

    # So far I have not figured out how to store the user type at the moment ((((
    none_user = 0
    admin_user = 1
    usual_user = 2
    type_of_user_now = int()

    def __init__(self, dbname: str, user: str, password: str, host: str):
        """
        Creation of an object for working with a database on the server.

        :param dbname: Database name.
        :param user: Username.
        :param password: User password.
        :param host: Server ip with db.
        """

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

        self.connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        self.cursor = self.connection.cursor()

    def check_user_pass(self, login: str, password: str) -> int:
        """
        Checks the presence of a user in the database.

        :param login: User login.
        :param password: User password.
        :return: User type (0 if not found).
        """

        query = "select type from {} where login=%s and password=%s"
        values = (login, password)

        self.cursor.execute(query.format(self.user_table_name), values)
        temp_list_type_of_users = self.cursor.fetchall()

        if len(temp_list_type_of_users) == 0:
            return 0
        else:
            return temp_list_type_of_users[0][0]

    def __del__(self):
        """
        Garbage removal - database connection and cursor.

        :return: None
        """

        self.connection.close()
        self.cursor.close()
