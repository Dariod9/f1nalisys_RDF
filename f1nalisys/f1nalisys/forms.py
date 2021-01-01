from django import forms


class Filter(forms.Form):
    races = forms.IntegerField(label="Races", required=False)
    wins = forms.IntegerField(label="Wins", required=False)
