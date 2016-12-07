from django import forms

class Repoform(forms.Form):
  repository=forms.CharField(max_length=100)

class Boardform(forms.Form):
  board=forms.CharField(max_length=100)
