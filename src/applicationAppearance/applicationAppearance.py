from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class MobileApp(App):
    def build(self):
        """
        Builds home screen.

        :return: None.
        """

        self.root = Builder.load_file("src/applicationAppearance/mainScreen.kv")

    def next_screen(self, screen_name: str):
        """
        Load the next screen.

        :param screen_name: Name of the required screen.
        :return: None.
        """

        screen_file_name = screen_name + ".kv"

        Builder.unload_file(screen_file_name)
        screen_now = Builder.load_file(screen_file_name)

        self.root.container.clear_widgets()
        self.root.container.add_widget(screen_now)


class RootWidget(BoxLayout):
    text_input_username = ObjectProperty(None)
    # TODO Разберись, зачем этот контейнер
    container = ObjectProperty(None)

    def button_sign_in(self):
        """
        "Login" button click handler.

        :return: None.
        """

        # TODO Нормальную проверку логина и пароля
        self.text_input_username.text = "ХУи"
