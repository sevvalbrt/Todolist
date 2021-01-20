import os
import sqlite3

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from Components.Login import Login
from Components.Notes import Notes
from Components.UpdateNote import UpdateNote


class SM(ScreenManager):
    userId=StringProperty("")
    note_id=StringProperty("")


    def __init__(self):
        super(SM, self).__init__()
        self.current="login"
        Notes.goto_updatenote=self.goto_updatenote


    def goto_updatenote(self,id):
        UpdateNote.note_id=id
        self.note_id=UpdateNote.note_id
        self.current = "updatenote"


