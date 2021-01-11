import os
import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from src.captcha import Captcha
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
    db.users_table_name = "users"
    db.guests_table_name = "guests"
    db.meetings_table_name = "meetings"

    # Screen container
    container = ObjectProperty(None)

    # Pop-up message
    popup_invalid_data = ObjectProperty(None)

    # Fields
    text_input_captcha = ObjectProperty(None)
    text_input_name = ObjectProperty(None)
    text_input_phone = ObjectProperty(None)
    text_input_email = ObjectProperty(None)
    text_input_date = ObjectProperty(None)
    text_input_list = ObjectProperty(None)
    text_input_login = ObjectProperty(None)
    text_input_password = ObjectProperty(None)
    text_input_user_type = ObjectProperty(None)

    # Variables to automatically update the list on some screens
    text_input_date_help = ObjectProperty(None)
    text_input_name_help = ObjectProperty(None)
    text_input_phone_help = ObjectProperty(None)

    # Variables to work with captcha
    captcha_text = str()
    captcha_image = ObjectProperty(None)
    button_new_captcha = ObjectProperty(None)

    # Variables to work with time
    first_time = None
    count_of_try = 0

    @staticmethod
    def check_correct_phone(phone: str) -> bool:
        """
        Checking the correctness of phone number.

        :param phone: Phone number to be checked.
        :return: Is phone number correct.
        """

        return len(phone) == 11

    @staticmethod
    def check_correct_date(date: str) -> bool:
        """
        Checks if date is entered correctly.

        :param date: Date to check.
        :return: Date is entered correctly.
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

    def login_in(self, login: str, password: str) -> None:
        """
        Trying to login in.

        :param login: User login from corresponding field.
        :param password: User password from corresponding field.
        :return: None.
        """

        if not self.text_input_captcha.disabled:
            if self.text_input_captcha.text == self.captcha_text:
                self.close_captcha()
            else:
                self.text_input_captcha.text = ''
                self.load_captcha()

            return

        self.db.type_of_user_now = self.db.login_in(login, password)

        if self.db.type_of_user_now == self.db.none_user:
            self.count_of_try += 1

            if self.first_time is None:
                self.first_time = datetime.datetime.now()
            else:
                delta_time = datetime.datetime.now() - self.first_time
                if int(delta_time.total_seconds() / 60) >= 60 and self.count_of_try >= 5:
                    self.start_captcha()

            self.popup_invalid_data.open()
        else:
            self.next_screen("screenWithGuestsList")

    def options(self) -> None:
        """
        Clicking on the options button.

        In some cases, you need to return to the standard user options screen (from the nested options).
        This function also implements this moment.

        :return: None.
        """

        if self.db.type_of_user_now == self.db.admin_user:
            self.next_screen("adminSettingsScreen")
        else:
            self.next_screen("usualSettingsScreen")

    def add_guest_to_db(self) -> None:
        """
        Adding a guest to database.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"
            return
        if self.text_input_name.text == '':
            self.text_input_name.text = "EMPTY FIELD"
            return
        if self.text_input_email.text == '':
            self.text_input_email.text = "EMPTY FIELD"
            return

        if self.db.add_guest_to_db(self.text_input_name.text, self.text_input_phone.text, self.text_input_email.text):
            self.text_input_name.text = ''
            self.text_input_phone.text = ''
            self.text_input_email.text = ''
        else:
            self.popup_invalid_data.open()

    def add_user_to_db(self) -> None:
        """
        Adding a user to database.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"
            return
        if self.text_input_user_type.text != '1' and self.text_input_user_type.text != '2':
            self.text_input_user_type.text = "Invalid type"
            return
        if self.text_input_name.text == '':
            self.text_input_name.text = "EMPTY FIELD"
            return
        if self.text_input_login.text == '':
            self.text_input_login.text = "EMPTY FIELD"
            return
        if self.text_input_password.text == '':
            self.text_input_password.text = "EMPTY FIELD"
            return
        if self.text_input_email.text == '':
            self.text_input_email.text = "EMPTY FIELD"
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

    def add_guest_to_meeting(self) -> None:
        """
        Adding a guest to meeting.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"
            return
        if not self.check_correct_date(self.text_input_date.text):
            self.text_input_date.text = "Invalid date"
            return

        if self.db.add_guest_to_meeting(self.text_input_phone.text, self.text_input_date.text):
            self.text_input_phone.text = ''
            self.text_input_date.text = ''
        else:
            self.popup_invalid_data.open()

    def delete_guest_from_db(self) -> None:
        """
        Delete guest from database.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"
            return

        self.db.delete_guest_from_db(self.text_input_phone.text)
        self.text_input_phone.text = ''

        self.show_list_of_all_guests_or_users(
            self.db.guests_table_name, self.text_input_name_help.text, self.text_input_phone_help.text
        )

    def delete_user_from_db(self) -> None:
        """
        Delete user from database.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"
            return

        self.db.delete_user_from_db(self.text_input_phone.text)
        self.text_input_phone.text = ''

        self.show_list_of_all_guests_or_users(
            self.db.users_table_name, self.text_input_name_help.text, self.text_input_phone_help.text
        )

    def delete_guest_from_meeting(self) -> None:
        """
        Delete guest from meeting.

        :return: None.
        """

        if not self.check_correct_phone(self.text_input_phone.text):
            self.text_input_phone.text = "Invalid number"
            return
        if not self.check_correct_date(self.text_input_date.text):
            self.text_input_date.text = "Invalid date"
            return

        self.db.delete_guest_from_meeting(self.text_input_phone.text, self.text_input_date.text)
        self.text_input_phone.text = ''
        self.text_input_date.text = ''

        self.show_list_of_guests(
            self.text_input_date_help.text, self.text_input_name_help.text, self.text_input_phone_help.text
        )

    def show_list_of_all_guests_or_users(self, table_name: str, name: str = '', phone: str = '') -> None:
        """
        Show list of all guest (names and phones).

        :param table_name: Name of the table from which to take data.
        :param name: Name to search by.
        :param phone: Phone number to search for.
        :return: None.
        """

        temp_list = self.db.get_name_phone_from_tables(table_name, name, phone)
        self.text_input_list.text = str()

        for line in temp_list:
            self.text_input_list.text += ' '.join(line) + '\n'

    def show_list_of_guests(self, date: str = '', name: str = '', phone: str = '') -> None:
        """
        Show list of guests on meetings.

        :param date: Date to search by.
        :param name: Name to find.
        :param phone: Phone to find.
        :return: None.
        """

        temp_list = self.db.get_list_of_guests_on_meetings(date, name, phone)
        self.text_input_list.text = str()

        for line in sorted(temp_list):
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

    def start_captcha(self) -> None:
        """
        Launches captcha for the first time.

        :return: None.
        """

        self.button_new_captcha.disabled = False
        self.text_input_captcha.disabled = False
        self.text_input_login.disabled = True
        self.text_input_password.disabled = True
        self.load_captcha()

    def load_captcha(self) -> None:
        """
        Loads captcha to the screen.

        :return: None.
        """

        captcha_image, self.captcha_text = Captcha.get_captcha()

        captcha_image.save("captcha.png")

        self.captcha_image.reload()

        os.remove("captcha.png")

    def close_captcha(self) -> None:
        """
        Closing fields for entering captcha. Opening fields for entering login and password.

        :return: None.
        """

        self.button_new_captcha.disabled = True
        self.text_input_captcha.disabled = True
        self.text_input_login.disabled = False
        self.text_input_password.disabled = False
