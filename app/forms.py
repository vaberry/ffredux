from django import forms
from .models import NewDocument

class DocumentForm(forms.ModelForm):
    class Meta:
        model = NewDocument
        fields = ('description', 'document', )