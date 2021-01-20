from kivy.properties import StringProperty
from kivy.uix.actionbar import ActionBar
from kivy.lang import Builder


class Menu(ActionBar):
    userId=StringProperty("")
    def __init__(self, **kwargs):
        super(Menu,self).__init__(**kwargs)

    def logout(self):
        pass

    def insert_note(self):
        pass

    def update_user(self,userId):
        pass

    def goto_notes(self):
        pass