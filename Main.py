from kivy.app import App
from kivy.lang import Builder

from Components.SM import SM
from Backend.Database import Database
from Components.Login import Login
from Components.InsertUser import InsertUser
from Components.Insertnote import Insertnote
from Components.UpdateUser import UpdateUser
from Components.UpdateNote import UpdateNote
from Components.Notes import Notes
from Components.NotePage import NotePage
from Components.Menu import Menu

Builder.load_file("Components/SM.kv")
Builder.load_file("Components/Login.kv")
Builder.load_file("Components/InsertUser.kv")
Builder.load_file("Components/Insertnote.kv")
Builder.load_file("Components/UpdateUser.kv")
Builder.load_file("Components/UpdateNote.kv")
Builder.load_file("Components/Notes.kv")
Builder.load_file("Components/NotePage.kv")
Builder.load_file("Components/Menu.kv")


class MainApp(App):

    def __init__(self,**kwargs):
        super(MainApp, self).__init__()

    def build(self):
        return SM()

if __name__=="__main__":
    MainApp().run()