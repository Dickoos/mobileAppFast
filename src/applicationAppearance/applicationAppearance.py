import csv
import os
import datetime

from string import digits
from typing import List, Dict
from xml.etree import ElementTree
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

from src.captcha import Captcha
from src.password import Password
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
    popup_error_data = ObjectProperty(None)
    popup_after_add_from_file = ObjectProperty(None)

    # Pop-up fields
    popup_text_input_name = ObjectProperty(None)
    popup_text_input_login = ObjectProperty(None)
    popup_text_input_password = ObjectProperty(None)
    popup_text_input_phone = ObjectProperty(None)
    popup_text_input_email = ObjectProperty(None)
    popup_text_input_user_type = ObjectProperty(None)

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

    # Variables to work with csv
    error_data = ListProperty()
    added_from_file = NumericProperty()

    @staticmethod
    def check_correct_phone(phone: str) -> bool:
        """
        Checking the correctness of phone number.

        :param phone: Phone number to be checked.
        :return: Is phone number correct.
        """

        if len(phone) != 11:
            return False

        for num in phone:
            if num not in digits:
                return False

        return True

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

    @staticmethod
    def get_csv_dict(filename: str) -> List[Dict[str, str]]:
        """
        Reads data from a csv file and returns a list with data.

        :param filename: Name of the file (along with the path).
        :return: Data list.
        """

        with open(filename, encoding="utf-8") as csv_file:
            return [dict(row) for row in csv.DictReader(csv_file, delimiter='/')]

    @staticmethod
    def get_xml_dict(filename: str) -> List[Dict[str, str]]:
        """
        Reads data from a xml file and returns a list with data.

        :param filename: Name of the file (along with the path).
        :return: Data list.
        """

        result = list()

        try:
            for contact in ElementTree.parse(filename).getroot():
                temp_dict = dict()
                for field in contact:
                    temp_dict.update({field.tag: field.text})
                result.append(temp_dict)
        except ElementTree.ParseError:
            result = list()

        return result

    @staticmethod
    def get_password(text_input: ObjectProperty) -> None:
        """
        Fills in the field with the prepared password.

        :param text_input: The field where you need to insert the password.
        :return: None.
        """

        text_input.text = Password.get_password()

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
                if int(delta_time.total_seconds() / 60) <= 60 and self.count_of_try >= 5:
                    self.start_captcha()
                elif int(delta_time.total_seconds() / 60) > 60:
                    self.first_time = None

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

        if not self.db.add_guest_to_db(self.text_input_name.text,
                                       self.text_input_phone.text,
                                       self.text_input_email.text):
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

        if not self.db.add_user_to_db(self.text_input_name.text, self.text_input_login.text,
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

    def add_user_to_db_from_error_popup(self) -> None:
        """
        Attempts to add a user to the database.

        :return: None.
        """

        self.make_all_popup_fields_white()

        if not self.check_correct_phone(self.popup_text_input_phone.text):
            self.popup_text_input_phone.text = "Invalid number"
            self.popup_text_input_phone.background_color = "red"
            return
        if self.popup_text_input_user_type.text != '1' and self.popup_text_input_user_type.text != '2':
            self.popup_text_input_user_type.text = "Invalid type"
            self.popup_text_input_user_type.background_color = "red"
            return
        if self.popup_text_input_name.text == '':
            self.popup_text_input_name.text = "EMPTY FIELD"
            self.popup_text_input_name.background_color = "red"
            return
        if self.popup_text_input_login.text == '':
            self.popup_text_input_login.text = "EMPTY FIELD"
            self.popup_text_input_login.background_color = "red"
            return
        if self.popup_text_input_password.text == '':
            self.popup_text_input_password.text = "EMPTY FIELD"
            self.popup_text_input_password.background_color = "red"
            return
        if self.popup_text_input_email.text == '':
            self.popup_text_input_email.text = "EMPTY FIELD"
            self.popup_text_input_email.background_color = "red"
            return

        if not self.db.add_user_to_db(self.popup_text_input_name.text, self.popup_text_input_login.text,
                                      self.popup_text_input_password.text, self.popup_text_input_phone.text,
                                      self.popup_text_input_email.text, self.popup_text_input_user_type.text):
            self.error_data.pop(0)
            self.added_from_file += 1
            if len(self.error_data):
                self.load_new_error_data_in_fields()
            else:
                self.popup_error_data.dismiss()
                self.popup_after_add_from_file.open()
        else:
            # Since we cannot say in which field the error is, we paint them in a different color just in case
            self.popup_text_input_email.background_color = "pink"
            self.popup_text_input_login.background_color = "pink"
            self.popup_text_input_phone.background_color = "pink"

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

        if not self.db.add_guest_to_meeting(self.text_input_phone.text, self.text_input_date.text):
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
        self.text_input_list.text = ''.join([' '.join(line) + '\n' for line in sorted(temp_list)])

    def show_list_of_guests(self, date: str = '', name: str = '', phone: str = '') -> None:
        """
        Show list of guests on meetings.

        :param date: Date to search by.
        :param name: Name to find.
        :param phone: Phone to find.
        :return: None.
        """

        temp_list = self.db.get_list_of_guests_on_meetings(date, name, phone)
        temp_list.sort(key=lambda line: datetime.datetime.strptime(line[0], '%d.%m.%Y'))
        self.text_input_list.text = ''.join([' '.join(line) + '\n' for line in temp_list])

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

    def load_file(self, filename: str) -> None:
        """
        Uploading csv/xml file with users.

        :param filename: File name.
        :return: None.
        """

        if filename[-3:] == "csv":
            data_list = self.get_csv_dict(filename)
        elif filename[-3:] == "xml":
            data_list = self.get_xml_dict(filename)
        else:
            self.popup_invalid_data.open()
            return

        # Silly file validation check.
        try:
            temp = data_list[0]["name"]
            temp = data_list[0]["login"]
            temp = data_list[0]["password"]
            temp = data_list[0]["phone"]
            temp = data_list[0]["email"]
            temp = data_list[0]["type"]
        except KeyError:
            self.popup_invalid_data.open()
            return
        except IndexError:
            self.popup_invalid_data.open()
            return

        self.error_data = []
        self.added_from_file = 0
        for row in data_list:
            all_right = True
            for key in row.keys():
                if row[key] is None:
                    row[key] = ''
                    all_right = False
                elif row[key] == '':
                    all_right = False

            if not all_right:
                self.error_data.append(row)
            elif self.db.add_user_to_db(*[row[key] for key in row.keys()]):
                # Since the check is carried out on the server, we can only guess in which fields the errors are.
                row["email"] = ''
                row["login"] = ''
                row["phone"] = ''

                self.error_data.append(row)
            else:
                self.added_from_file += 1

        if len(self.error_data) != 0:
            self.popup_error_data.open()
            self.load_new_error_data_in_fields()

    def load_new_error_data_in_fields(self) -> None:
        """
        Loads new data with errors into fields.

        :return: None.
        """

        zero_row = self.error_data[0]

        self.popup_text_input_name.text = zero_row["name"]
        if zero_row["name"] == '' or zero_row["name"] is None:
            self.popup_text_input_name.background_color = "red"

        self.popup_text_input_login.text = zero_row["login"]
        if zero_row["login"] == '' or zero_row["login"] is None:
            self.popup_text_input_login.background_color = "red"

        self.popup_text_input_password.text = zero_row["password"]
        if zero_row["password"] == '' or zero_row["password"] is None:
            self.popup_text_input_password.background_color = "red"

        self.popup_text_input_phone.text = zero_row["phone"]
        if zero_row["phone"] == '' or zero_row["phone"] is None:
            self.popup_text_input_phone.background_color = "red"

        self.popup_text_input_email.text = zero_row["email"]
        if zero_row["email"] == '' or zero_row["email"] is None:
            self.popup_text_input_email.background_color = "red"

        self.popup_text_input_user_type.text = zero_row["type"]
        if zero_row["type"] == '' or zero_row["type"] is None:
            self.popup_text_input_user_type.background_color = "red"

    def make_all_popup_fields_white(self) -> None:
        """
        Returns all fields to a fine white color.

        :return: None.
        """

        self.popup_text_input_name.background_color = "white"
        self.popup_text_input_login.background_color = "white"
        self.popup_text_input_password.background_color = "white"
        self.popup_text_input_phone.background_color = "white"
        self.popup_text_input_email.background_color = "white"
        self.popup_text_input_user_type.background_color = "white"
