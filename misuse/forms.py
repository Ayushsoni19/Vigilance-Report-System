from django import forms
from .models import MisuseEntry

class MisuseEntryForm(forms.ModelForm):
    class Meta:
        model = MisuseEntry
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
