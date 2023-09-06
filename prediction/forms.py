from django import forms

class PredictionForm(forms.Form):
    protocol = forms.IntegerField()
    sourcePort = forms.IntegerField()
    destPort = forms.IntegerField()
    size = forms.IntegerField()
    seqNumber = forms.IntegerField()
    ackNumber = forms.IntegerField()
