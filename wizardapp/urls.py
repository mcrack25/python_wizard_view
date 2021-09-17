from django.urls import path
from .views import WelcomeWizard_as, WelcomeWizard_ls

urlpatterns = [
    path('', WelcomeWizard_as.as_view(WelcomeWizard_as._form_list, condition_dict=WelcomeWizard_as._condition_dict), name='welcomeform_autosave_first',),
    path('autosave/', WelcomeWizard_as.as_view(WelcomeWizard_as._form_list, condition_dict=WelcomeWizard_as._condition_dict), name='welcomeform_autosave',),
    path('latesave/', WelcomeWizard_ls.as_view(WelcomeWizard_ls._form_list, condition_dict=WelcomeWizard_ls._condition_dict), name='welcomeform_latesave',),
]
