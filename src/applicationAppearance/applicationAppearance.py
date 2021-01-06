from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from src.authorization import Authorization


class MobileApp(App):
    def build(self) -> None:
        """
        Builds home screen.

        :return: None.
        """

        self.root = Builder.load_file("src/applicationAppearance/mainScreen.kv")


class RootWidget(BoxLayout):
    container = ObjectProperty(None)

    popup = ObjectProperty(None)

    text_input_username = ObjectProperty(None)
    text_input_password = ObjectProperty(None)

    def button_sign_in(self) -> None:
        """
        "Login" button click handler.

        :return: None.
        """

        # TODO Нормальную проверку логина и пароля
        type_of_user = Authorization.check_user_pass(self.text_input_username.text, self.text_input_password.text)

        if type_of_user == Authorization.none_user:
            self.popup.open()
        elif type_of_user == Authorization.admin_user:
            self.next_screen("adminScreen")
        elif type_of_user == Authorization.usual_user:
            # TODO Экран для обычного пользователя
            pass

    def next_screen(self, screen_name: str) -> None:
        """
        Load the next screen.

        :param screen_name: Name of the required screen.
        :return: None.
        """

        screen_file_name = "src/applicationAppearance/" + screen_name + ".kv"

        Builder.unload_file(screen_file_name)
        screen_now = Builder.load_file(screen_file_name)

        self.container.clear_widgets()
        self.container.add_widget(screen_now)

    def view_guests_list(self, date: str, name: str, phone: str) -> None:
        """
        Creates a guest list from buttons (collective farm, but how else?).

        :param date: Date to search by.
        :param name: The name to find.
        :param phone: Phone to find.
        :return: None.
        """

        # TODO реализуй нормальный список
        pass
