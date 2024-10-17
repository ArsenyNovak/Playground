from django import forms

class FeedbackMessageForm(forms.Form):
     message = forms.CharField(widget=forms.Textarea(attrs={'cols': 55, 'rows': 5}), label='Сообщение')