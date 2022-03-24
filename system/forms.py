from django import forms

class SysconfigForm(forms.Form):
    CHOICES = (
        ("MP3", "MP3"),
        ("WMA", "WMA"),
    )
    audiotype = forms.ChoiceField(label='音频存储格式',choices=CHOICES)
    channel1 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel1')
    channel2 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel2')
    channel3 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel3')
    channel4 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel4')

class UsrForm(forms.Form):
    CHOICES = (
        ("管理员", "管理员"),
        ("操作员", "操作员"),
    )
    usr_perssions = forms.ChoiceField(label='用户权限',choices=CHOICES)
    usrname = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), label='用户名', max_length=100,required=True)
    password_one = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'请输入密码','class':'single_line'}), label='密码', max_length=100,required=True)
    password_two = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'请再次输入密码','class':'single_line'}), label='密码校验', max_length=100,required=True)
    usrname_n = forms.CharField(widget=forms.TextInput)
    usr_perssions_n = forms.CharField(widget=forms.TextInput)


