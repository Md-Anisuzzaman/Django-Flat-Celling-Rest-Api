from django.urls import path, include
# from projectmanagement import views
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectsModelViewSet,
    ProjectDocumentsModelViewSet,
    ProjectCustomersModelViewSet,
    ProjectCustomerInformationModelViewSet,
    ProjectPaymentsModelViewSet,
    project_details_with_customers,
    # customer_details,
    ProjectWithSingleCustomerDetailView
)

router = DefaultRouter()
router.register('projects', ProjectsModelViewSet)
router.register('project-documents', ProjectDocumentsModelViewSet)
router.register('project-customers', ProjectCustomersModelViewSet)
router.register('project-customer-info',
                ProjectCustomerInformationModelViewSet)
router.register('project-payments', ProjectPaymentsModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_id>/customers/',
         project_details_with_customers, name='project-detail-with-customers'),
    # path('projects/<int:project_id>/customers/<int:customer_id>/',
    #      customer_details, name='customer-detail'),
    path('projects/<int:project_pk>/customer/<int:customer_pk>/',
         ProjectWithSingleCustomerDetailView, name='project-with-single-customer-detail'),
]


# urlpatterns = [
#     path('projects/',ProjectsModelViewSet.as_view()),

# ]
