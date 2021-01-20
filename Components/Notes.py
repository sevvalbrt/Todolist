import calendar
import datetime
from datetime import date
import sqlite3
from functools import partial

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from Components.UpdateNote import UpdateNote
from Components.UpdateUser import UpdateUser
from Components.Menu import Menu
from Backend.Database import Database
from Components.NotePage import NotePage


class Notes(Screen):
    userId=StringProperty("")
    note_id=StringProperty("")
    def __init__(self,**kwargs):
        super(Notes, self).__init__()
        self.DB=Database()
        Menu.logout = self.logout
        Menu.update_user = self.update_user
        Menu.insert_note = self.insert_note
        Menu.goto_notes=self.goto_notes
        NotePage.update_note=self.update_note
        NotePage.popup=self.deletePopup

        Clock.schedule_interval(self.reminder, 10)

    def on_enter(self, *args):
        x=datetime.datetime.now()
        year=x.strftime("%y")
        self.userId = self.manager.userId
        self.ids.container.clear_widgets()
        con=sqlite3.connect(self.DB.DB_PATH)
        cursor=con.cursor()
        x=("select * from Notes where UserId= "+str(self.userId)+"")
        cursor.execute(x)
        result=cursor.fetchall()
        for i in result:
            wid=NotePage()
            r2=' Subject: '+i[2]+'\n'+' Note: '+i[3]+'\n'+' Clock: '+str(i[4])+":"+str(i[5])+'\n'+' Date: '+str(i[6])+"/"+str(i[7]+"/"+year)
            wid.note_id=str(i[0])
            wid.note=r2
            self.ids.container.add_widget(wid)

        con.close()


    def reminder(self,id):
        box = BoxLayout(orientation='vertical')
        now = datetime.datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        x3 = ("select * from Notes where Hour='"+hour+"' and Minute= '"+minute+"' and Day='"+day+"' and Month='"+month+"'")
        cursor.execute(x3)
        result = cursor.fetchall()
        for nots in result:
            subject=nots[2]
            note=nots[3]
            box.add_widget(Image(source="Images/reminder.png"))
            box.add_widget(Label(text="Subject: "+subject, bold=True, italic=True))
            box.add_widget(Label(text="Note: "+note, bold=True, italic=True))

            deleteButton = Button(text="Delete",id="element"+str(nots[0]),bold=True,italic=True)
            deleteButton.bind(on_release=partial(self.delete_note,nots[0]))
            box.add_widget(deleteButton)

            editButton= Button(text="PostPone",bold=True,italic=True)
            editButton.bind(on_press=partial(self.Postpone,nots[0]))
            box.add_widget(editButton)

            self.popUp = Popup(title='',
                          content=box,
                          size_hint=(None, None), size=(400, 400),
                          auto_dismiss=False)

            self.popUp.open()

    def delete_note(self,id,instance):
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        s = "delete from Notes where NoteId='" + str(id) + "'"
        cursor.execute(s)
        con.commit()
        con.close()
        for child in self.ids.container.children:
            if str(child.note_id)==str(id):
                self.ids.container.remove_widget(child)
                self.popUp.dismiss()


    def delete_note_fromPopup(self,id,instance):
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        s = "delete from Notes where NoteId='" + id + "'"
        cursor.execute(s)
        con.commit()
        con.close()
        for child in self.ids.container.children:
            if child.note_id==id:
                self.ids.container.remove_widget(child)
                self.popup.dismiss()


    def deletePopup(self,id):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Image(source="Images/question.png"))
        box.add_widget(Label(text="Are you sure you want to delete this note?", bold=True, italic=True))
        self.popup = Popup(title=" ",
                           content=box,
                           size_hint=(None, None), size=(350, 350),
                           auto_dismiss=False)

        deleteButton = Button(text="YES", bold=True, italic=True)
        deleteButton.bind(on_press=partial(self.delete_note_fromPopup,id))
        box.add_widget(deleteButton)
        box.add_widget(Button(text="NO", bold=True, italic=True, on_press=self.popup.dismiss))
        self.popup.open()

    def logout(self):
        self.manager.current="login"

    def update_user(self,userId):
        UpdateUser.userId=self.manager.userId
        self.manager.current="updateuser"

    def insert_note(self):
        self.manager.current="insertnote"

    def update_note(self,note_id):
        self.goto_updatenote(note_id)

    def update_notePopup(self,note_id,instance):
        self.manager.current="updatenote"
        self.popUp.dismiss()
    def goto_notes(self):
        self.manager.current="notes"
    def goto_updatenote(self):
        pass
    def Postpone(self,id,instance):
        x=5
        now = datetime.datetime.now()
        minute = now.strftime("%M")
        hour=now.strftime("%H")
        day = now.strftime("%d")
        month = now.strftime("%m")
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        minute=int(minute)+x
        TotalDays = calendar.monthrange(now.year, now.month)[1]
        if minute>=60:
            eklenecek = minute - 60
            minute= 00 + eklenecek
            minute=("{:02d}".format(minute))
            hour=int(hour)+1
            if hour>=24:
                hour=hour-24
                hour = ("{:02d}".format(hour))
                day=int(day)+1
                if day>TotalDays:
                    day=day-TotalDays
                    day = ("{:02d}".format(day))
                    month=int(month)+1
                    if month>12:
                        month=1
                        month = ("{:02d}".format(month))
            x1=(hour,minute,day,month)
            s3 = 'update Notes set '
            s4 = 'Hour="%s", Minute="%s",Day="%s",Month="%s"' % x1
            s5 = ' where NoteId=%s' % id
            cursor.execute(s3 + s4 + s5)
            con.commit()
            con.close()
            self.popUp.dismiss()
            self.on_enter(instance)
        else:
            minute = ("{:02d}".format(minute))
            s = 'update Notes set '
            s1 = ' Minute="%s"' % minute
            s2 = ' where NoteId=%s' % id
            cursor.execute(s + s1 +s2)
            con.commit()
            con.close()
            self.popUp.dismiss()
            self.on_enter(instance)


