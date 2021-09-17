from django import forms, inlineformset_factory
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

MessagesInlineFormSet = inlineformset_factory(Person, Messages, fields=('text',), extra=2, )