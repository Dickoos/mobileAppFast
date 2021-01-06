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

        self.title = "Monitoring event attendance"
        self.root = Builder.load_file("src/applicationAppearance/mainScreen.kv")


class RootWidget(BoxLayout):
    # Screen container
    container = ObjectProperty(None)

    # Pop-up message on login screen
    popup_invalid_username_or_password = ObjectProperty(None)

    # Login screen fields
    text_input_username = ObjectProperty(None)
    text_input_password = ObjectProperty(None)
    # Fields of the main admin window
    text_input_list_guests = ObjectProperty(None)

    def button_sign_in(self) -> None:
        """
        "Login" button click handler.

        :return: None.
        """

        # TODO Нормальную проверку логина и пароля
        Authorization.type_of_user_now = Authorization.check_user_pass(self.text_input_username.text, self.text_input_password.text)

        if Authorization.type_of_user_now == Authorization.none_user:
            self.popup_invalid_username_or_password.open()
        else:
            self.next_screen("screenWithGuestsList")

    def button_options(self) -> None:
        """
        Handling of pressing the option button (in order not to spoil the .kv file with an ugly if).

        In some cases, you need to return to the standard user options screen (from the nested options).
        This function also implements this moment.

        :return: None.
        """

        if Authorization.type_of_user_now == Authorization.admin_user:
            self.next_screen("adminSettingsScreen")
        else:
            self.next_screen("usualSettingsScreen")

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

    def view_guests_list(self, date: str = '', name: str = '', phone: str = '') -> None:
        """
        Creates a guest list from buttons (collective farm, but how else?).

        :param date: Date to search by.
        :param name: The name to find.
        :param phone: Phone to find.
        :return: None.
        """

        # TODO реализуй нормальный список
        test_str_list = str()
        for i in range(500):
            test_str_list += (str(i) + " line test\n")
        self.text_input_list_guests.text = test_str_list
