from django import forms

class SysconfigForm(forms.Form):
    CHOICES = (
        (1, "MP3"),
        (2, "WMA"),
    )
    audiotype = forms.ChoiceField(label='音频存储格式',choices=CHOICES)
    channel1 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel1')
    channel2 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel2')
    channel3 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel3')
    channel4 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False,label='channel4')