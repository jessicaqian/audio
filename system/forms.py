from django import forms

class SysconfigForm(forms.Form):
    CHOICES = (
        ("mp3", "MP3"),
        ("wav", "WAV"),
    )
    CHOICES1 = (
        ("全时段录音", "全时段录音"),
        ("自动录音", "自动录音"),
    )

    audiotype = forms.ChoiceField(label='音频存储格式',choices=CHOICES)
    audiomode = forms.ChoiceField(label='录音模式',choices=CHOICES1)
    audiotime = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line','value':'10'}), required=False,label='音频文件存储时间')
    channel1 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel1')
    channel2 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel2')
    channel3 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel3')
    channel4 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel4')
    channel5 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel5')
    channel6 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel6')
    channel7 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel7')
    channel8 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel8')
    channel9 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel9')
    channel10 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel10')
    channel11 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel11')
    channel12 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel12')
    channel13 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel13')
    channel14 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel14')
    channel15 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel15')
    channel16 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel16')
    channel17 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel17')
    channel18 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel18')
    channel19 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel19')
    channel20 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel20')
    channel21 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel21')
    channel22 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel22')
    channel23 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel23')
    channel24 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel24')
    channel25 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel25')
    channel26 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel26')
    channel27 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel27')
    channel28 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel28')
    channel29 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel29')
    channel30 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel30')
    channel31 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel31')
    channel32 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel32')
    channel33 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel33')
    channel34 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel34')
    channel35 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel35')
    channel36 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel36')
    channel37 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel37')
    channel38 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel38')
    channel39 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel39')
    channel40 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel40')
    channel41 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel41')
    channel42 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel42')
    channel43 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel43')
    channel44 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel44')
    channel45 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel45')
    channel46 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel46')
    channel47 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel47')
    channel48 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel48')
    channel49 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel49')
    channel50 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel50')
    channel51 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel51')
    channel52 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel52')
    channel53 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel53')
    channel54 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel54')
    channel55 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel55')
    channel56 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel56')
    channel57 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel57')
    channel58 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel58')
    channel59 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel59')
    channel60 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel60')
    channel61 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel61')
    channel62 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel62')
    channel63 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel63')
    channel64 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='channel64')
    usrname_n = forms.CharField(widget=forms.TextInput)
    usr_perssions_n = forms.CharField(widget=forms.TextInput)

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

class NetForm(forms.Form):
    ip = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    mask = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    netgate = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    usrname_n = forms.CharField(widget=forms.TextInput)
    usr_perssions_n = forms.CharField(widget=forms.TextInput)





