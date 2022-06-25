from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields."""

    class Meta:
        model = MyUser
        fields = ('discord_id', 'discord_name', 'discord_discriminator')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user.
    """

    class Meta:
        model = MyUser
        fields = ('discord_id', 'discord_name', 'discord_discriminator', 'is_active', 'is_superuser')

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the MyUser model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('discord_id', 'discord_name', 'discord_discriminator', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('discord_id',)}),
        ('Personal info', {'fields': ('discord_name', 'discord_discriminator')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('discord_id', 'discord_name', 'discord_discriminator'),
        }),
    )
    search_fields = ('discord_name',)
    ordering = ('discord_name',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.

#I think I am using django's build in permissions...
#admin.site.unregister(Group)
