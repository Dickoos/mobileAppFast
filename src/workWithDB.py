import psycopg2


class DB:
    dbname = str()
    user = str()
    password = str()
    host = str()
    connection = None
    cursor = None

    user_table_name = str()
    guests_table_name = str()
    meetings_table_name = str()

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

        query = "select type from {} where login=%s and password=%s".format(self.user_table_name)
        values = (login, password)

        self.cursor.execute(query, values)
        temp_list_type_of_users = self.cursor.fetchall()

        if len(temp_list_type_of_users) == 0:
            return 0
        else:
            return temp_list_type_of_users[0][0]

    def add_person_to_db(self, name: str, phone: str, email: str) -> bool:
        """
        Adds a person to the database.

        :param name: Name of person.
        :param phone: Person's phone.
        :param email: Email of person.
        :return: Whether the recording went well.
        """

        if name == '' or phone == '' or email == '':
            return False

        query = "insert into {} values (%s, %s, %s)".format(self.guests_table_name)
        values = (name, phone, email)

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except psycopg2.errors.UniqueViolation:
            self.connection.commit()
            return False

        return True

    def add_person_to_meeting(self, phone: str, date: str) -> bool:
        """
        Allows you to add a guest to the meeting.

        :param phone: Guest phone number (recording is possible only if the guest is in the database).
        :param date: Date of the event (in the format day.month.year).
        :return: Whether the recording was successful.
        """

        if phone == '' or date == '':
            return False

        query = "insert into {} values (%s, %s)".format(self.meetings_table_name)
        values = (phone, date)

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except psycopg2.errors.UniqueViolation:
            self.connection.commit()

            return False
        except psycopg2.errors.ForeignKeyViolation:
            self.connection.commit()

            return False

        return True

    def get_name_phone_from_guests(self, name: str, phone: str) -> list:
        """
        Returns the list of guest - phone number.

        :param name: The name by which to search.
        :param phone: The phone number to search for.
        :return: A list of names and phone numbers.
        """

        query = "select name, phone from {}".format(self.guests_table_name)
        if name != '' and phone != '':
            query += " where name = %s and phone = %s"
            values = (name, phone)
        elif name != '':
            query += " where name = %s"
            values = (name, )
        elif phone != '':
            query += " where phone = %s"
            values = (phone, )
        else:
            values = ()

        print(query, values)
        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def __del__(self):
        """
        Garbage removal - database connection and cursor.

        :return: None
        """

        self.connection.close()
        self.cursor.close()
