class Authorization:
    @staticmethod
    def check_user_pass(username: str, password: str) -> bool:
        """
        Checks username and password on the server.

        :param username: Username.
        :param password: User password.
        :return: Is a match found in the database.
        """

        # TODO Проверка на сервере
        true_username = "admin"
        true_password = "admin"

        if username == true_username and password == true_password:
            return True
        else:
            return False
