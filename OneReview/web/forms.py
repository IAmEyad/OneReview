from django import forms

class QueryForm(forms.Form):
    search = forms.CharField(label="You're input", max_length=100)