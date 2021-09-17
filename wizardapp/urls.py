from django.urls import path
from .views import WelcomeWizard_as

urlpatterns = [
    path('autosave/', WelcomeWizard_as.as_view(WelcomeWizard_as._form_list, condition_dict=WelcomeWizard_as._condition_dict), name='welcomeform_autosave',),
]
