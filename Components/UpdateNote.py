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

class UpdateNote(Screen):
    note_id=StringProperty("")
    def __init__(self,**kwargs):
        super(UpdateNote, self).__init__()
        self.DB=Database()

    def on_enter(self, *args):
        con=sqlite3.connect(self.DB.DB_PATH)
        cursor=con.cursor()
        s="select Subject,Note,Hour,Minute,Day,Month from Notes where NoteId='"
        cursor.execute(s+self.note_id + "'")
        result=cursor.fetchall()
        for i in result:
            self.ids.ti_subject.text=i[0]
            self.ids.ti_note.text = i[1]
            self.ids.hour.text=i[2]
            self.ids.minute.text=i[3]
            self.ids.day.text=i[4]
            self.ids.month.text=i[5]
        con.close()

    def update_note(self):
        now = datetime.datetime.now()
        Day = now.strftime("%d")
        Month = now.strftime("%m")
        Hour= now.strftime("%H")
        Minute = now.strftime("%M")
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_subject.text
        d2 = self.ids.ti_note.text
        d3 = self.ids.hour.text
        d4 = self.ids.minute.text
        d5 = self.ids.day.text
        d6 = self.ids.month.text
        a1 = (d1,d2,d3,d4,d5,d6)
        s1 = 'update Notes set'
        s2 = 'Subject="%s",Note="%s",Hour="%s",Minute="%s",Day="%s",Month="%s"' % a1
        s3='where NoteId=%s' % self.note_id
        try:
            if '' in a1:
                box2=BoxLayout(orientation="vertical")
                box2.add_widget(Image(source="Images/attention.png"))
                box2.add_widget(Label(text="One or more fields are empty \n\n    Please fill in all fields",bold=True,italic=True))
                popUp2=Popup(title=" ",
                           content=box2,
                           size_hint=(None, None), size=(300, 300),
                           auto_dismiss=True)
                closeButton=Button(text="Close",bold=True,italic=True,on_press=popUp2.dismiss,size_hint_y=0.3)
                box2.add_widget(closeButton)
                popUp2.open()
            else:
                if(d6<Month or (d6<=Month and d5<Day) or (d6<=Month and d5<=Day and d3<Hour) or (d6<=Month and d5<=Day and d3<=Hour and d4<Minute)):
                    box3 = BoxLayout(orientation="vertical")
                    box3.add_widget(Image(source="Images/attention.png"))
                    box3.add_widget(Label(text="You have selected a past date or time \n\n   Please select another date or time", bold=True,italic=True))
                    popUp3 = Popup(title=" ",
                                  content=box3,
                                  size_hint=(None, None), size=(300, 300),
                                  auto_dismiss=True)
                    closeButton = Button(text="Close", bold=True, italic=True, on_press=popUp3.dismiss, size_hint_y=0.3)
                    box3.add_widget(closeButton)
                    popUp3.open()
                else:
                    cursor.execute(s1 + ' ' + s2+' '+s3)
                    con.commit()
                    con.close()
                    self.goto_notes()
        except Exception as e:
            print("e")
            con.close()

    def popup(self):
        pass

    def goto_notes(self):
        self.manager.current="notes"