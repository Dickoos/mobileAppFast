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

    def add_user_to_db(self, name: str, login: str, password: str, phone: str, email: str, type_of_user: str) -> bool:
        """
        Allows to add a user to the database.

        :param name: User's real name.
        :param login: User login.
        :param password: User password.
        :param phone: User's phone number (must be unique).
        :param email: User's email.
        :param type_of_user: User type (1 - admin, 2 - regular user).
        :return: Did you manage to record.
        """

        if name == '' or login == '' or password == '' or phone == '' or email == '' or type_of_user == '':
            return False

        query = "insert into {} values (%s, %s, %s, %s, %s, %s)".format(self.user_table_name)
        values = (name, login, password, phone, email, type_of_user)

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except psycopg2.errors.UniqueViolation:
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
        values = list()

        if name != '':
            query += " where name = %s"
            values.append(name)
        if phone != '':
            if query[-2] != '%':
                query += " where phone = %s"
            else:
                query += " and phone = %s"

            values.append(phone)

        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def get_name_phone_from_users(self, name: str, phone: str) -> list:
        """
        Returns the list of users - phone number.

        :param name: The name by which to search.
        :param phone: The phone number to search for.
        :return: A list of names and phone numbers.
        """

        query = "select name, phone from {}".format(self.user_table_name)
        values = list()

        if name != '':
            query += " where name = %s"
            values.append(name)
        if phone != '':
            if query[-2] != '%':
                query += " where phone = %s"
            else:
                query += " and phone = %s"

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

        query = "select date, name, {0}.phone from {0}, {1} where {1}.phone = {0}.phone".format(
            self.guests_table_name, self.meetings_table_name
        )
        values = list()

        if date != '':
            query += " and date = %s"
            values.append(date)
        if name != '':
            query += " and name = %s"
            values.append(name)
        if phone != '':
            query += " and {}.phone = %s".format(self.guests_table_name)
            values.append(phone)

        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def delete_person_from_db(self, phone: str) -> None:
        """
        Removes a person from the database (along with appointments).

        :param phone: The phone number of the person to be deleted.
        :return: None.
        """

        query = "delete from {0} where phone = %(phone)s; delete from {1} where phone = %(phone)s;".format(
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

        query = "delete from {} where phone = %s".format(self.user_table_name)
        values = (phone, )

        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_person_from_meeting(self, phone: str, date: str) -> None:
        """
        Removes a person from a specific meeting.

        :param phone: Person's phone.
        :param date: Meeting date.
        :return: None.
        """

        query = "delete from {} where phone = %s and date = %s".format(self.meetings_table_name)
        values = (phone, date)

        self.cursor.execute(query, values)
        self.connection.commit()

    def __del__(self):
        """
        Garbage removal - database connection and cursor.

        :return: None
        """

        self.connection.close()
        self.cursor.close()
