from django import forms
from .models import Person, Messages

class FLNameForm(forms.ModelForm):
    no_sname = forms.BooleanField(required=False, label='Нет отчества')
    class Meta:
        model = Person
        fields = (
            'lname',
            'fname',
        )

class SNameForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = (
            'sname',
        )

MessagesInlineFormSet = forms.inlineformset_factory(Person, Messages, fields=('text',), extra=2, can_delete=False)