from django.shortcuts import render
from .models import Person, Messages
from .forms import FLNameForm, SNameForm, MessagesInlineFormSet
from formtools.wizard.views import SessionWizardView

STEP_ONE = '0'
STEP_TWO = '1'
STEP_THREE = '2'

class WelcomeWizard_as(SessionWizardView):
    template_name = 'wizardapp/form.html'
    person = Person()

    def add_to_db(self, step):
        if step == STEP_ONE:
            data_step = self.get_cleaned_data_for_step(step)
            self.person.fname = data_step['fname']
            self.person.lname = data_step['lname']
            self.person.save()
        elif step == STEP_TWO:
            formset = MessagesInlineFormSet(self.request.POST, self.request.FILES, instance=self.person,
                                            prefix=step)
            for form in formset:
                if form.is_valid():
                    form.save(commit=False)
            if formset.is_valid():
                abc = formset.save()
                print(abc)
        elif step == STEP_THREE:
            data_step = self.get_cleaned_data_for_step(step)
            self.person.sname = data_step['sname']
            self.person.save()


    def done(self, form_list, **kwargs):
        self.add_to_db(self.steps.current)

        # Сбрасываем состояние модели
        self.person.pk = None
        self.person.adding = True

        return render(self.request, 'wizardapp/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        self.add_to_db(self.steps.prev)
        return context

    # Custom methods
    def return_true(self):
        return True

    def check_step_3(self):
        result = True
        step_info = self.get_cleaned_data_for_step(STEP_ONE)
        try:
            if (step_info['no_sname']):
                result = False
        except:
            pass
        return result

    _condition_dict = {
        STEP_ONE: return_true,
        STEP_TWO: return_true,
        STEP_THREE: check_step_3,
    }

    _form_list = [
        (STEP_ONE, FLNameForm),
        (STEP_TWO, MessagesInlineFormSet),
        (STEP_THREE, SNameForm),
    ]

