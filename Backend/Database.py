import os

from kivy.uix.screenmanager import Screen


class Database(Screen):
    def __init__(self):
        super(Database, self).__init__()
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH + "/todolist.db"