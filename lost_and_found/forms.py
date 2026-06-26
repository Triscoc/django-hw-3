from django import forms 
from .models import LostTable

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostTable
        fields = ['name', 'location', 'description', 'is_returned']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What item?'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where?'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'is_returned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or name.strip() == '':
            raise forms.ValidationError('Item name cannot be empty')
        return name

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if len(location) < 2:
            raise forms.ValidationError('Location is too short')
        return location
