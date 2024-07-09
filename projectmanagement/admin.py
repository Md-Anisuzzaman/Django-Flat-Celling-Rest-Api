from django.contrib import admin
from .models import ProjectsModel, ProjectCustomerInformationModel, ProjectDocumentsModel, ProjectPaymentsModel, ProjectCustomersModel


@admin.register(ProjectsModel)
class ProjectsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'p_id', 'title', 'per_share_cost',
                    'address', 'created_at', 'updated_at')
    list_display_links = ('title',)


@admin.register(ProjectDocumentsModel)
class ProjectDocumentsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'file_type',
                    'upload_file', 'url', 'created_at', 'updated_at')
    list_display_links = ('id',)


@admin.register(ProjectCustomersModel)
class ProjectCustomersModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'user_id', 'total_share',
                    'have_to_pay_amount', 'paid', 'created_at', 'updated_at')
    list_display_links = ('id',)


@admin.register(ProjectCustomerInformationModel)
class ProjectCustomerInformationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_customer_id', 'customer_name',
                    'customer_phone1', 'customer_nominee_name', 'created_at', 'updated_at')
    list_display_links = ('id',)


@admin.register(ProjectPaymentsModel)
class ProjectPaymentsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'user_id', 'payment_type',
                    'amount', 'created_at', 'updated_at')
    list_display_links = ('id',)


# admin.site.register(ProjectsModel,ProjectsModelAdmin)
# admin.site.register(ProjectDocumentsModel,ProjectDocumentsModelAdmin)
# admin.site.register(ProjectCustomersModel,ProjectCustomersModelAdmin)
# admin.site.register(ProjectCustomerInformationModel,ProjectCustomerInformationModelAdmin)
# admin.site.register(ProjectPaymentsModel,ProjectPaymentsModelAdmin)
