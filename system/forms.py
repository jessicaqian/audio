from django import forms

class SysconfigForm(forms.Form):
    CHOICES = (
        ("mp3", "MP3"),
        ("wav", "WAV"),
    )


    audiotype = forms.ChoiceField(label='音频存储格式',choices=CHOICES)
    audiotime = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line','value':'10'}), required=False,label='音频文件存储时间')
    path = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=True,label='文件存储路径')
    usrname_n = forms.CharField(widget=forms.TextInput)
    usr_perssions_n = forms.CharField(widget=forms.TextInput)




class ChannelForm(forms.Form):
    CHOICES = (
        ("全时段录音", "全时段录音"),
        ("自动录音", "自动录音"),
    )

    channelNo = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=True,label='通道号')
    audiomode = forms.ChoiceField(label='录音模式',choices=CHOICES)
    channelname = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='通道名')
    recordval = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='开始录音阈值')
    mutetime = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=True,label='停止录音时长')
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





