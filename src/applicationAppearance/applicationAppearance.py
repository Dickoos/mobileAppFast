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
    db.meetings_table_name = "meetings"

    # Screen container
    container = ObjectProperty(None)

    # Pop-up message on login screen
    popup_invalid_username_or_password = ObjectProperty(None)
    # Pop-up message on add person
    popup_invalid_data = ObjectProperty(None)

    # Fields of the main admin window
    text_input_list_guests = ObjectProperty(None)
    # Fields of the add person
    text_input_name = ObjectProperty(None)
    text_input_phone = ObjectProperty(None)
    text_input_email = ObjectProperty(None)
    text_input_date = ObjectProperty(None)
    text_input_list = ObjectProperty(None)
    text_input_login = ObjectProperty(None)
    text_input_password = ObjectProperty(None)
    text_input_user_type = ObjectProperty(None)

    # Variables to automatically update the list on some screens
    date_text = ObjectProperty(None)
    name_text = ObjectProperty(None)
    phone_text = ObjectProperty(None)

    @staticmethod
    def check_correct_phone(phone: str) -> bool:
        """
        Checking the correctness of the number.

        :param phone: The number to be checked.
        :return: Either the number is correct or not.
        """

        return len(phone) == 11 or (len(phone) == 12 and phone[0] == '+')

    @staticmethod
    def check_correct_date(date: str) -> bool:
        """
        Checks if the date is entered correctly.

        :param date: The date to check.
        :return: The date is entered correctly.
        """

        try:
            day, month, year = map(int, date.split('.'))
        except ValueError:
            return False
        day_str, month_str, year_str = date.split('.')

        if day < 1 or day > 31 or len(day_str) != 2:
            return False
        if month < 1 or month > 12 or len(month_str) != 2:
            return False
        if year < 1000 or len(year_str) < 4:
            return False

        return True

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

    def button_add_user_to_db(self) -> None:
        """
        Processing the button for adding a user to the database.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"

            return
        if '1' < self.text_input_user_type.text > '2':
            self.text_input_user_type.text = "Invalid type"

            return

        if self.db.add_user_to_db(self.text_input_name.text, self.text_input_login.text,
                                  self.text_input_password.text, self.text_input_phone.text,
                                  self.text_input_email.text, self.text_input_user_type.text):
            self.text_input_name.text = ''
            self.text_input_login.text = ''
            self.text_input_password.text = ''
            self.text_input_phone.text = ''
            self.text_input_email.text = ''
            self.text_input_user_type.text = ''
        else:
            self.popup_invalid_data.open()

    def button_add_person_to_meeting(self) -> None:
        """
        Handling a key press for adding a person to a meeting.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"

            return
        if not self.check_correct_date(self.text_input_date.text):
            self.text_input_date.text = "Invalid date"

            return

        if self.db.add_person_to_meeting(self.text_input_phone.text, self.text_input_date.text):
            self.text_input_phone.text = ''
            self.text_input_date.text = ''
        else:
            self.popup_invalid_data.open()

    def button_delete_person_from_db(self) -> None:
        """
        Handler for pressing the button to delete a person from the database.

        :return: None.
        """

        self.db.delete_person_from_db(self.text_input_phone.text)
        self.text_input_phone.text = ''

        self.button_find_in_add_person_to_meeting(self.name_text.text, self.phone_text.text)

    def button_delete_user_from_db(self) -> None:
        """
        Handling pressing the button to remove a user from the database.

        :return: None.
        """

        self.db.delete_user_from_db(self.text_input_phone.text)
        self.text_input_phone.text = ''

        self.button_find_users(self.name_text.text, self.phone_text.text)

    def button_delete_person_from_meeting(self) -> None:
        """
        Handling a button to remove a person from a meeting.

        :return: None.
        """

        self.db.delete_person_from_meeting(self.text_input_phone.text, self.text_input_date.text)
        self.text_input_phone.text = ''
        self.text_input_date = ''

        self.view_guests_list(self.date_text.text, self.name_text.text, self.phone_text.text)

    def button_find_in_add_person_to_meeting(self, name: str = '', phone: str = '') -> None:
        """
        Handles a click on the search button on the add guest to meeting screen.

        :param name: The name to search by.
        :param phone: The phone number to search for.
        :return: None.
        """

        temp_list = self.db.get_name_phone_from_guests(name, phone)
        self.text_input_list.text = str()

        for line in temp_list:
            self.text_input_list.text += ' '.join(line) + '\n'

    def button_find_users(self, name: str = '', phone: str = '') -> None:
        """
        Handles a click on the search button on the add guest to meeting screen.

        :param name: The name to search by.
        :param phone: The phone number to search for.
        :return: None.
        """

        temp_list = self.db.get_name_phone_from_users(name, phone)
        self.text_input_list.text = str()

        for line in temp_list:
            self.text_input_list.text += ' '.join(line) + '\n'

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

        temp_list = self.db.get_list_of_guests_on_meetings(date, name, phone)
        self.text_input_list_guests.text = str()

        for line in sorted(temp_list):
            self.text_input_list_guests.text += ' '.join(line) + '\n'
