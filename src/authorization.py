class Authorization:
    none_user = 0
    admin_user = 1
    usual_user = 2

    @staticmethod
    def check_user_pass(username: str, password: str) -> int:
        """
        Checks username and password on the server.

        :param username: Username.
        :param password: User password.
        :return: Database user type (if any).
        """

        # TODO Проверка на сервере

        true_admin_user = "admin"
        true_admin_pass = "admin"
        true_usual_user = "usual"
        true_usual_pass = "usual"

        if username == true_admin_user and password == true_admin_pass:
            return Authorization.admin_user
        elif username == true_usual_user and password == true_usual_pass:
            return Authorization.usual_user
        else:
            return Authorization.none_user
