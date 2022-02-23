from django import forms
import hashlib
import sqlite3

class NameForm(forms.Form):
    usrname = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='密码', max_length=100)



    def clean(self):
        username=self.cleaned_data['usrname']
        password=self.cleaned_data['password']
        m = password + "{{sdtzzq}}"
        pw = hashlib.md5(m.encode())


        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = " SELECT str FROM usradmin "
        cursor.execute(sql)
        val = cursor.fetchall()
        muser = val[0]
        mpw = val[1]

        if (muser[0] == username)&(mpw[0] == pw.hexdigest()):
            pass
        else:
             raise forms.ValidationError(u"用户名或密码错误，请重新输入")

        conn.close()

        return self