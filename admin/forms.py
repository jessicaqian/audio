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


class RegisterRorm(forms.Form):

    gender = (
        ('male',"男"),
        ('female',"女"),
    )

    username = forms.CharField(label="用户名",max_length=56,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="密码",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱",widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label="性别",choices=gender)
    captcha = forms.CharField(label="验证码")


