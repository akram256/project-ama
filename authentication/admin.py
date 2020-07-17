import csv
from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse


from .models import User,Age_Category,UserProfile
# from rangefilter.filter import DateRangeFilter

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        """ Refer to comment on line 34"""
        # field_names = [field.name for field in meta.fields]
        field_names = [ 'Email', 'First Name', 'Last Name']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=lottoly-user-{}.csv'.format(datetime.now())
        writer = csv.writer(response)

        writer.writerow(field_names)
        """ Commented this out to handle the logic better for making this export feature more generic"""
        # for obj in queryset:
        #     row = writer.writerow([getattr(obj, field) for field in field_names])

        users = User.objects.all().values_list( 'email','first_name', 'last_name')
        for user in users:
            writer.writerow(user)

        return response

    export_as_csv.short_description = "Export as Csv"

class CustomUserAdmin(UserAdmin, ExportCsvMixin):
    list_display = ('id',  'email','first_name', 'last_name','role',
                    'created_at')
    list_filter = ('created_at','is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('created_at',)
    fieldsets = (
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser')}),
    )
    actions = ["export_as_csv"]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Age_Category)
admin.site.register(UserProfile)


# @admin.register(School)
# class SchoolAdmin(admin.ModelAdmin):
#     list_display = ('school_email','school_name','school_address',)
#     # list_filter = ( ('created_at',DateRangeFilter),)
#     search_fields = ('created_at','school_email','school_name')

admin.site.site_header = "AMA Admin Portal"
admin.site.site_title = "AMA Admin Portal"
admin.site.index_title = "Welcome to AMA Admin Portal"



