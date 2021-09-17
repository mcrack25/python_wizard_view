from django.contrib import admin
from .models import Person, Messages

class PersonAdmin(admin.ModelAdmin):
    pass

class MessagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Messages, MessagesAdmin)