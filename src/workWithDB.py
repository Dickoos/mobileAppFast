import psycopg2


class DB:
    # Connection data
    database_name = str()
    user = str()
    password = str()
    host = str()

    # Variables for accessing the database
    connection = None
    cursor = None

    # Table names
    users_table_name = str()
    guests_table_name = str()
    meetings_table_name = str()

    # User types
    none_user = 0
    admin_user = 1
    usual_user = 2
    # The type of user who is logged in
    type_of_user_now = int()

    def __init__(self, database_name: str, user: str, password: str, host: str):
        """
        Creation of an object for working with a database on the server.

        :param database_name: Database name.
        :param user: Username.
        :param password: User password.
        :param host: Server ip with database.
        """

        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host

        self.connection = psycopg2.connect(
            dbname=self.database_name, user=self.user,
            password=self.password, host=self.host
        )
        self.cursor = self.connection.cursor()

    def login_in(self, login: str, password: str) -> int:
        """
        Checks the presence of a user in the database.

        :param login: User login.
        :param password: User password.
        :return: User type (0 if not found).
        """

        query = "SELECT type_id FROM {} WHERE login = %s and password = %s".format(self.users_table_name)
        values = (login, password)

        self.cursor.execute(query, values)
        type_of_user = self.cursor.fetchone()

        if type_of_user is None:
            return self.none_user
        else:
            return type_of_user[0]

    def add_guest_to_db(self, name: str, phone: str, email: str) -> int:
        """
        Add a guest to database.

        :param name: Name of person.
        :param phone: Person's phone.
        :param email: Email of person.
        :return: 0 - everything is fine, 1 - uniqueness error, 2 - phone number error.
        """

        query = "INSERT INTO {} (name, phone, email) VALUES (%s, %s, %s)".format(self.guests_table_name)
        values = [name, phone, email]

        return self.try_to_insert_in_db(query, values)

    def add_user_to_db(self, name: str, login: str, password: str, phone: str, email: str, type_of_user: str) -> int:
        """
        Add user to database.

        :param name: User's real name.
        :param login: User login.
        :param password: User password.
        :param phone: User's phone number (must be unique).
        :param email: User's email.
        :param type_of_user: User type (1 - admin, 2 - regular user).
        :return: 0 - everything is fine, 1 - uniqueness error, 2 - phone number error.
        """

        query = "INSERT INTO {} (name, login, password, phone, email, type_id) VALUES (%s, %s, %s, %s, %s, %s)"
        query = query.format(self.users_table_name)
        values = [name, login, password, phone, email, type_of_user]

        return self.try_to_insert_in_db(query, values)

    def add_guest_to_meeting(self, phone: str, date: str) -> int:
        """
        Add guest to meeting.

        :param phone: Guest phone number (recording is possible only if the guest is in the database).
        :param date: Date of the event (in the format day.month.year).
        :return: 0 - everything is fine, 1 - uniqueness error, 2 - phone number error.
        """

        query = "INSERT INTO {} (phone, date) VALUES (%s, %s)".format(self.meetings_table_name)
        values = [phone, date]

        return self.try_to_insert_in_db(query, values)

    def get_name_phone_from_tables(self, table_name: str, name: str, phone: str) -> list:
        """
        Returns the list of name - phone number.

        :param table_name: Name of table in which to search.
        :param name: The name by which to search.
        :param phone: The phone number to search for.
        :return: A list of names and phone numbers.
        """

        query = "SELECT name, phone FROM {}".format(table_name)
        values = list()

        if name != '':
            query += " WHERE name = %s"
            values.append(name)
        if phone != '':
            if query[-2] != '%':
                query += " WHERE phone = %s"
            else:
                query += " AND phone = %s"
            values.append(phone)

        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def get_list_of_guests_on_meetings(self, date: str, name: str, phone: str) -> list:
        """
        Returns a list of guests.

        :param date: The date by which the search is required.
        :param name: The name by which to search.
        :param phone: The phone number to search for.
        :return: Guest list (date - name - phone number).
        """

        query = "SELECT date, name, {0}.phone FROM {0}, {1} WHERE {1}.phone = {0}.phone".format(
            self.guests_table_name, self.meetings_table_name
        )
        values = list()

        if date != '':
            query += " AND date = %s"
            values.append(date)
        if name != '':
            query += " AND name = %s"
            values.append(name)
        if phone != '':
            query += " AND {}.phone = %s".format(self.guests_table_name)
            values.append(phone)

        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def delete_guest_from_db(self, phone: str) -> None:
        """
        Removes a person from the database (along with meetings).

        :param phone: The phone number of the guest to be deleted.
        :return: None.
        """

        query = "DELETE FROM {0} WHERE phone = %(phone)s; DELETE FROM {1} WHERE phone = %(phone)s;".format(
            self.meetings_table_name, self.guests_table_name
        )
        values = {"phone": phone}

        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_user_from_db(self, phone: str) -> None:
        """
        Removing a user from the database.

        :param phone: User number to be deleted.
        :return: None.
        """

        query = "DELETE FROM {} WHERE phone = %s".format(self.users_table_name)
        values = [phone]

        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_guest_from_meeting(self, phone: str, date: str) -> None:
        """
        Removes a guest from meeting.

        :param phone: Person's phone.
        :param date: Meeting date.
        :return: None.
        """

        query = "DELETE FROM {} WHERE phone = %s AND date = %s".format(self.meetings_table_name)
        values = [phone, date]

        self.cursor.execute(query, values)
        self.connection.commit()

    def try_to_insert_in_db(self, query: str, values: list) -> int:
        """
        Trying to write something to database.

        :param query: Request text.
        :param values: Variables required for request.
        :return: 0 - everything is fine, 1 - uniqueness error, 2 - phone number error.
        """

        all_right = 0

        try:
            self.cursor.execute(query, values)
        except psycopg2.errors.UniqueViolation as error:
            all_right = 1
            print(error)
        except psycopg2.errors.ForeignKeyViolation:
            all_right = 2

        self.connection.commit()

        return all_right

    def __del__(self):
        """
        Garbage removal - database connection and cursor.

        :return: None.
        """

        self.connection.close()
        self.cursor.close()
