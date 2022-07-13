from django import forms
import hashlib
# import sqlite3
import configparser

class NameForm(forms.Form):
    usrname = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='密码', max_length=100)



    def clean(self):
        username=self.cleaned_data['usrname']
        password=self.cleaned_data['password']
        m = password + "{{sdtzzq}}"
        pw = hashlib.md5(m.encode())
        config = configparser.ConfigParser()

        config.read("web.ini")

        try:
            name = config.get(username, "name")
            psw = config.get(username, "pw")

            if (name == username)&(psw == pw.hexdigest()):
                pass



            else:
                 raise forms.ValidationError(u"用户名或密码错误，请重新输入")
        except:
            raise forms.ValidationError(u"用户名或密码错误，请重新输入")



        # conn = sqlite3.connect('db.sqlite3')
        # cursor = conn.cursor()
        # sql = " SELECT usrname,psword FROM usradmin WHERE usrname='"+username+"'"
        # cursor.execute(sql)
        # val = cursor.fetchone()
        # if val == None:
        #     raise forms.ValidationError(u"用户名或密码错误，请重新输入")
        # else:
        #     muser = val[0]
        #     mpw = val[1]
        #
        #     if (muser == username)&(mpw == pw.hexdigest()):
        #         pass
        #
        #
        #     else:
        #          raise forms.ValidationError(u"用户名或密码错误，请重新输入")
        #
        # conn.close()

        return self.cleaned_data