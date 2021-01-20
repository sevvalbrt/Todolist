import sqlite3

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from Backend.Database import Database

class InsertUser(Screen):
    def __init__(self,**kwargs):
        super(InsertUser, self).__init__()
        self.DB=Database()

    def insert_user(self):
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_name.text
        d2 = self.ids.ti_lastname.text
        d3 = self.ids.ti_username.text
        d4 = self.ids.ti_password.text
        a1 = (d1, d2, d3, d4)
        s1 = 'insert into Users(Name,LastName,UserName,Password)'
        s2 = 'values("%s","%s","%s","%s")' % a1
        try:
            if '' in a1:
                box5=BoxLayout(orientation="vertical")
                box5.add_widget(Image(source="Images/attention.png"))
                box5.add_widget(Label(text="One or more fields are empty \n\n    Please fill in all fields",bold=True,italic=True))
                popup5=Popup(title="",
                             content=box5,
                             size_hint=(None, None), size=(300, 300),
                             auto_dismiss=False)
                closeButton=Button(text="Close",bold=True,italic=True,on_press=popup5.dismiss,size_hint_y=0.4)
                box5.add_widget(closeButton)
                popup5.open()
            else:
                x="select * from Users where UserName='"+d3+"'"
                cursor.execute(x)
                result=cursor.fetchall()
                if result:
                    box6=BoxLayout(orientation="vertical")
                    box6.add_widget(Image(source="Images/attention.png"))
                    box6.add_widget(Label(text="This username is used by someone else\n  Please specify another username",bold=True,italic=True))
                    popup6=Popup(title="",
                                 content=box6,
                                 size_hint=(None, None), size=(300, 300),
                                 auto_dismiss=False)
                    CloseButton=Button(text="Close",bold=True,italic=True,on_press=popup6.dismiss,size_hint_y=.3)
                    box6.add_widget(CloseButton)
                    popup6.open()
                else:
                    cursor.execute(s1 + s2)
                    con.commit()
                    con.close()
                    self.popup1()
        except Exception as e:
            print("e")


    def popup1(self):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Image(source="Images/checked.png"))
        box.add_widget(Label(text="Your membership has been successfully completed",bold=True,italic=True))
        popup1 = Popup(title="",
                            content=box,
                            size_hint=(None, None), size=(400, 400),
                            auto_dismiss=False)
        btn = Button(text="Close",bold=True,italic=True,size_hint_y=0.4,on_press=popup1.dismiss)
        box.add_widget(btn)
        popup1.open()

    def cleartext(self):
        self.ids.ti_name.text=''
        self.ids.ti_lastname.text=''
        self.ids.ti_username.text=''
        self.ids.ti_password.text=''







