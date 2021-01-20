import sqlite3

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from Backend.Database import Database

class NotePage(BoxLayout):
    def __init__(self,**kwargs):
        super(NotePage, self).__init__()
        self.DB=Database()

    def update_note(self):
        pass

    def popup(self):
        pass