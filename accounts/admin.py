from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser


class UserAdmin(UserAdmin):
    
    # Standard Functionality
    date_hierarchy = 'date_joined'
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    #Standard as per Django
    default_add_fields = ('username', 'password1', 'password2')
    default_display = ['username', 'email', 'first_name', 'last_name', 'is_staff',]
    dfault_filter = ['is_staff','is_superuser','is_active',]
    
    # Custom inheritance functionality
    custom_fields = {}
    add_fields = []
    list_fields = []
    filter_fields = []

    new_fields = ()
    existing_fieldsets =[]
    new_fields = []

    # Create a dict from model settings with fieldset name as key
    # And the list of fields as value
    for field in model._meta.get_fields():
        if field.__dict__.get('is_registration') == True:
                add_fields.append(field.__dict__.get('name'))
        if field.__dict__.get('is_list_display') == True:
                list_fields.append(field.__dict__.get('name'))
        if field.__dict__.get('is_list_filter') == True:
                filter_fields.append(field.__dict__.get('name'))
        if field.__dict__.get('is_custom') == True:
            fset = field.__dict__.get('fieldset')
            if fset in custom_fields:
                custom_fields[fset].append(field.__dict__.get('name'))
            else:
                custom_fields[fset] = [field.__dict__.get('name')]

    
    #Append to existing fieldsets
    for fieldset in list(UserAdmin.fieldsets):
        if fieldset[0] != None and fieldset[0] in custom_fields:
            new_fields.append((fieldset[0],
                               {'fields': tuple(list(fieldset[1]['fields']) 
                                + list(custom_fields[fieldset[0]]))
                               }))
            existing_fieldsets.append(fieldset[0])
        else:
            new_fields.append(fieldset)

    #Add new fieldsets
    
    for new_fieldset, new_field in  custom_fields.items():
        if new_fieldset not in existing_fieldsets:
            new_fields.append((new_fieldset,
                               {'fields': tuple(new_field)
                               }))
    
    # The below settings are used to select the fields in the admin pages for
    # The displayed fields on the change form
    fieldsets = tuple(new_fields)
    # In the list display
    list_display = default_display + list_fields
    # In the list filter
    list_filter = dfault_filter + filter_fields
    # In the registration form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': default_add_fields + tuple(add_fields)}
         ),
    )

admin.site.register(CustomUser, UserAdmin)