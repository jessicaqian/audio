from django import forms
import hashlib
# import sqlite3
import configparser

class NameForm(forms.Form):
    usrname = forms.CharField(label='用户名', max_length=100,
                              widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入您的用户名','autofocus':''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入您的密码'}),
                               label='密码', max_length=100)

    def clean(self):
        username = self.cleaned_data['usrname']
        password = self.cleaned_data['password']
        m = password + "{{sdtzzq}}"
        pw = hashlib.md5(m.encode())
        config = configparser.ConfigParser()

        config.read("web.ini")

        try:
            name = config.get(username, "name")
            psw = config.get(username, "pw")

            if (name == username) & (psw == pw.hexdigest()):
                pass

            else:
                raise forms.ValidationError(u"用户名或密码错误，请重新输入")
        except:
            raise forms.ValidationError(u"用户名或密码错误，请重新输入")
            return self.cleaned_data
