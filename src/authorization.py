class Authorization:
    @staticmethod
    def check_user_pass(user_name: str, password: str):
        """
        Checks username and password on the server.

        :param user_name: Username.
        :param password: User password.
        :return: Is a match found in the database.
        """

        # TODO Проверка на сервере
        print(user_name, password)
