from reversion import VersionAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import models as auth_models
from front import models


# User management

class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class UserProfileAdmin(VersionAdmin):

    def has_change_permission(self, request, obj=None):
        """Limit change permission to own profile for non-superusers."""
        has_class_permission = super(UserProfileAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.pk != obj.user.pk:
            return False
        return True

    def queryset(self, request):
        """Only show own profile for non-superusers."""
        if request.user.is_superuser:
            return models.UserProfile.objects.all()
        return models.UserProfile.objects.filter(user=request.user)


admin.site.unregister(auth_models.User)
admin.site.register(auth_models.User, UserAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)


# Other model admin registrations

class AssignmentAdmin(VersionAdmin):
    date_hierarchy = 'date'
    list_display = ('User', 'date', 'unfulfilled')
    list_filter = ('User', 'unfulfilled')
    exclude_for_nonsuperuser = ('unfulfilled',)

    def add_view(self, request, *args, **kwargs):
        """Exclude additional fields for nonsuperusers when adding an object."""
        if not request.user.is_superuser:
            # Set current user as default value for user field
            data = request.GET.copy()
            data['User'] = request.user
            request.GET = data
            # Exclude some fields
            if self.exclude:
                self.exclude += self.exclude_for_nonsuperuser
            self.exclude = self.exclude_for_nonsuperuser
        return super(AssignmentAdmin, self).add_view(request, *args, **kwargs)

    def change_view(self, request, *args, **kwargs):
        """Exclude additional fields for nonsuperusers when changing an object."""
        if not request.user.is_superuser:
            if self.exclude:
                self.exclude += self.exclude_for_nonsuperuser
            self.exclude = self.exclude_for_nonsuperuser
        return super(AssignmentAdmin, self).change_view(request, *args, **kwargs)

    def has_change_permission(self, request, obj=None):
        """Limit change permission to own entries for non-superusers."""
        has_class_permission = super(AssignmentAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.pk != obj.User.pk:
            return False
        return True

    def queryset(self, request):
        """Only show own entries for non-superusers."""
        if request.user.is_superuser:
            return models.Assignment.objects.all()
        return models.Assignment.objects.filter(User=request.user)


class SemesterAdmin(VersionAdmin):
    list_display = ('year', 'season', 'start_date', 'end_date')
    list_filter = ('year', 'season')


admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Semester, SemesterAdmin)
