import os
import sys

from kivy.resources import resource_add_path

from src.applicationAppearance.applicationAppearance import MobileApp

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    MobileApp().run()
