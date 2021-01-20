import datetime
import sqlite3

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from Backend.Database import Database
from Components.Menu import Menu


class Insertnote(Screen):
    userId = StringProperty("")
    def __init__(self,**kwargs):
        super(Insertnote, self).__init__()
        self.DB=Database()

    def on_enter(self, *args):
        self.ids.ti_subject.text = ""
        self.ids.ti_note.text = ""
        self.ids.hour.text=""
        self.ids.minute.text=""
        self.ids.day.text=""
        self.ids.month.text=""

    def insert_note(self):
        self.userId=self.manager.userId
        now = datetime.datetime.now()
        Day = now.strftime("%d")
        Month = now.strftime("%m")
        Hour = now.strftime("%H")
        Minute = now.strftime("%M")
        con=sqlite3.connect(self.DB.DB_PATH)
        cursor=con.cursor()
        d2 = self.ids.ti_subject.text
        d3 = self.ids.ti_note.text
        d4 = self.userId
        d5 = self.ids.hour.text
        d6 = self.ids.minute.text
        d7 = self.ids.day.text
        d8 = self.ids.month.text
        a1=(d4,d2,d3,d5,d6,d7,d8)
        s1='insert into Notes(UserId,Subject,Note,Hour,Minute,Day,Month)'
        s2='values(%s,"%s","%s","%s","%s","%s","%s")' % a1
        try:
            if '' in a1:
                box=BoxLayout(orientation="vertical")
                box.add_widget(Image(source="Images/attention.png"))
                box.add_widget(Label(text="One or more fields are empty \n\n    Please fill in all fields",bold=True,italic=True))
                popUp=Popup(title=" ",
                           content=box,
                           size_hint=(None, None), size=(300, 300),
                           auto_dismiss=True)
                closeButton=Button(text="Close",bold=True,italic=True,on_press=popUp.dismiss,size_hint_y=0.3)
                box.add_widget(closeButton)
                popUp.open()
            else:
                if(d8<Month or (d8<=Month and d7<Day) or (d8<=Month and d7<=Day and d5<Hour) or (d8<=Month and d7<=Day and d5<=Hour and d6<Minute)):
                    box1 = BoxLayout(orientation="vertical")
                    box1.add_widget(Image(source="Images/attention.png"))
                    box1.add_widget(Label(text="You have selected a past date or time \n\n   Please select another date or time", bold=True,
                              italic=True))
                    popUp1 = Popup(title=" ",
                                  content=box1,
                                  size_hint=(None, None), size=(300, 300),
                                  auto_dismiss=True)
                    closeButton = Button(text="Close", bold=True, italic=True, on_press=popUp1.dismiss, size_hint_y=0.3)
                    box1.add_widget(closeButton)
                    popUp1.open()
                else:
                    cursor.execute(s1+s2)
                    con.commit()
                    con.close()
                    self.goto_notes()
        except Exception as e:
            print("e")

    def goto_notes(self):
        self.manager.current = "notes"