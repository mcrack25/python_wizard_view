from django.shortcuts import render
from .models import Person
from .forms import FLNameForm, SNameForm, MessagesInlineFormSet
from formtools.wizard.views import SessionWizardView

STEP_ONE = '0'
STEP_TWO = '1'
STEP_THREE = '2'

# Автоматическое сохранение данных на каждом шаге
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


# Сохранение данных в конце
class WelcomeWizard_ls(SessionWizardView):
    template_name = 'wizardapp/form.html'

    def gen_request(self, data, step):
        count_forms = str(len(data))
        del_items = ['DELETE', 'person']

        result = {
            '{0}-TOTAL_FORMS'.format(step): count_forms,
            '{0}-INITIAL_FORMS'.format(step): '0',
            '{0}-MIN_NUM_FORMS'.format(step): '0',
            '{0}-MAX_NUM_FORMS'.format(step): '1000',
        }
        i = 0
        for item in data:
            new_item = {}
            for el in item:
                if not (el in del_items):
                    key = '{0}-{1}-{2}'.format(step, i, el)
                    if item[el] == None:
                        val = ''
                    else:
                        val = item[el]
                    new_item.update({key: val})
            result.update(new_item)
            i += 1
        return result

    def done(self, form_list, **kwargs):
        step_1 = self.get_cleaned_data_for_step(STEP_ONE)
        step_2 = self.get_cleaned_data_for_step(STEP_TWO)
        step_3 = self.get_cleaned_data_for_step(STEP_THREE)

        person = Person()
        person.fname = step_1['fname']
        person.lname = step_1['lname']
        if step_3:
            person.sname = step_3['sname']
        person.save()

        req = self.gen_request(step_2, STEP_TWO)
        formset = MessagesInlineFormSet(req, self.request.FILES, instance=person, prefix=STEP_TWO)
        for form in formset:
            if form.is_valid():
                form.save(commit=False)
        if formset.is_valid():
            formset.save()

        return render(self.request, 'wizardapp/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

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