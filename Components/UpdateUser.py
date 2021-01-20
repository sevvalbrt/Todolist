import sqlite3

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from Backend.Database import Database
from Components.Menu import Menu


class UpdateUser(Screen):
    userId=StringProperty("")
    def __init__(self,**kwargs):
        super(UpdateUser, self).__init__()
        self.DB=Database()

    def on_enter(self, *args):
        con=sqlite3.connect(self.DB.DB_PATH)
        cursor=con.cursor()
        s="select Name,LastName,UserName,Password from Users where UserId='"
        cursor.execute(s+self.userId+"'")
        result=cursor.fetchall()
        for i in result:
            self.ids.ti_name.text =i[0]
            self.ids.ti_lastname.text = i[1]
            self.ids.ti_username.text = i[2]
            self.ids.ti_password.text = i[3]
        con.close()

    def update_user(self):
        con = sqlite3.connect(self.DB.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_name.text
        d2 = self.ids.ti_lastname.text
        d3 = self.ids.ti_username.text
        d4 = self.ids.ti_password.text
        a1 = (d1,d2,d3,d4)
        s1 = 'update Users set'
        s2 = 'Name="%s",LastName="%s",UserName="%s",Password="%s"' % a1
        s3 = 'where UserId=%s' % self.userId
        try:
            cursor.execute(s1 + ' ' + s2 + ' ' + s3)
            con.commit()
            con.close()
            self.goto_notes()
        except Exception as e:
            print("e")
            con.close()

    def goto_notes(self):
        self.manager.current="notes"


