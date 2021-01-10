from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from src.workWithDB import DB


class MobileApp(App):
    def build(self) -> None:
        """
        Builds home screen.

        :return: None.
        """

        self.title = "Monitoring event attendance"
        self.root = Builder.load_file("src/applicationAppearance/mainScreen.kv")


class RootWidget(BoxLayout):
    # Variable for working with db
    db = DB("test", "pi", "23514317", "192.168.1.69")
    db.user_table_name = "users"
    db.guests_table_name = "guests"

    # Screen container
    container = ObjectProperty(None)

    # Pop-up message on login screen
    popup_invalid_username_or_password = ObjectProperty(None)
    # Pop-up message on add person to db screen
    popup_invalid_data = ObjectProperty(None)

    # Fields of the main admin window
    text_input_list_guests = ObjectProperty(None)
    # Fields of the add person to db screen
    text_input_name = ObjectProperty(None)
    text_input_phone = ObjectProperty(None)
    text_input_email = ObjectProperty(None)

    def button_sign_in(self, login: str, password: str) -> None:
        """
        "Login" button click handler.

        :param login: User login from the corresponding field.
        :param password: User password from the corresponding field.
        :return: None.
        """

        self.db.type_of_user_now = self.db.check_user_pass(login, password)

        if self.db.type_of_user_now == self.db.none_user:
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

        if self.db.type_of_user_now == self.db.admin_user:
            self.next_screen("adminSettingsScreen")
        else:
            self.next_screen("usualSettingsScreen")

    def button_add_person_to_db(self) -> None:
        """
        Handling a button click to add a person to the database.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"
            return

        if self.db.add_person_to_db(self.text_input_name.text, self.text_input_phone.text, self.text_input_email.text):
            self.text_input_name.text = ''
            self.text_input_phone.text = ''
            self.text_input_email.text = ''
        else:
            self.popup_invalid_data.open()

    @staticmethod
    def check_correct_phone(phone: str) -> bool:
        """
        Checking the correctness of the number.

        :param phone: The number to be checked.
        :return: Either the number is correct or not.
        """

        return len(phone) == 11 or (len(phone) == 12 and phone[0] == '+')

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
