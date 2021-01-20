import sqlite3

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from Backend.Database import Database
from Components.InsertUser import InsertUser

class Login(Screen):
    userId=StringProperty("")
    def __init__(self,**kwargs):
        super(Login, self).__init__()
        self.DB=Database()

    def login(self):
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        x1 = self.ids.ti_username.text
        x2 = self.ids.ti_password.text
        bul=("select * from Users where UserName= ? and Password= ?")
        cursor.execute(bul,[(x1),(x2)])
        result=cursor.fetchall()
        if result:
            self.userId=str(result[0][0])
            self.manager.userId=self.userId
            for i in result:
                self.goto_notes()
        else:
            box4=BoxLayout(orientation="vertical")
            box4.add_widget(Image(source="Images/attention.png"))
            box4.add_widget(Label(text="Incorrect or in completed entry \n\n Please check your information",bold=True,italic=True))
            popup4=Popup(title="",
                         content=box4,
                         size_hint=(None, None), size=(300, 300),
                         auto_dismiss=False)
            closeButton=Button(text="Close",bold=True,italic=True,size_hint_y=0.4,on_press=popup4.dismiss)
            box4.add_widget(closeButton)
            popup4.open()
        con.close()

    def goto_notes(self):
        self.manager.current="notes"

    def on_enter(self, *args):
        self.ids.ti_username.text=''
        self.ids.ti_password.text=''


