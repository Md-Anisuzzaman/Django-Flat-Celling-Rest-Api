from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils import global_response

from .models import (
    ProjectsModel,
    ProjectDocumentsModel,
    ProjectCustomersModel,
    ProjectCustomerInformationModel,
    ProjectPaymentsModel,
)
from .serializersTwo import (
    ProjectsModelSerializer,
    ProjectDocumentsModelSerializer,
    ProjectCustomersModelSerializer,
    ProjectCustomerInformationModelSerializer,
    ProjectPaymentsModelSerializer,
    ProjectDetailSerializer,
    # DetailedCustomerSerializer,
    SingleCustomerDetailsSerializer
)


@api_view(['GET'])
def project_details_with_customers(request, project_id):
    try:
        project = ProjectsModel.objects.get(pk=project_id)
    except ProjectsModel.DoesNotExist:
        return global_response(errors="Project not found", status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectDetailSerializer(project)
    return global_response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def customer_details(request, project_id, customer_id):
    try:
        project = ProjectsModel.objects.get(pk=project_id)
    except ProjectsModel.DoesNotExist:
        return global_response(errors="Requested project not exist", status=status.HTTP_404_NOT_FOUND)

    try:
        customer = ProjectCustomersModel.objects.get(
            pk=customer_id, project_id=project_id)
    except ProjectCustomersModel.DoesNotExist:
        return global_response(errors="Customer hasn't any relation with this request project", status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectDetailSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ProjectWithSingleCustomerDetailView(request, project_pk, customer_pk, format=None):
    try:
        project = ProjectsModel.objects.get(pk=project_pk)
    except ProjectsModel.DoesNotExist:
        return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        customer = ProjectCustomersModel.objects.get(
            project_id=project, id=customer_pk)
    except ProjectCustomersModel.DoesNotExist:
        return Response({"detail": "Customer not found in this project."}, status=status.HTTP_404_NOT_FOUND)

    project_data = ProjectsModelSerializer(project).data
    print(project_data)
    customer_data = SingleCustomerDetailsSerializer(customer).data

    # Combine the project data with the specific customer data
    project_data['customer'] = customer_data

    return Response(project_data)


class ProjectsModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectsModelSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return global_response(msg="data deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return global_response(msg="Request data not exist", errors=str(e), status=status.HTTP_400_BAD_REQUEST)


class ProjectDocumentsModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocumentsModel.objects.all()
    serializer_class = ProjectDocumentsModelSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return global_response(msg="data deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return global_response(msg="Request data not exist", errors=str(e), status=status.HTTP_400_BAD_REQUEST)


class ProjectCustomersModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectCustomersModel.objects.all()
    serializer_class = ProjectCustomersModelSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return global_response(msg="data deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return global_response(msg="Request data not exist", errors=str(e), status=status.HTTP_400_BAD_REQUEST)


class ProjectCustomerInformationModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectCustomerInformationModel.objects.all()
    serializer_class = ProjectCustomerInformationModelSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return global_response(msg="data deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return global_response(msg="Request data not exist", errors=str(e), status=status.HTTP_400_BAD_REQUEST)


class ProjectPaymentsModelViewSet(viewsets.ModelViewSet):
    queryset = ProjectPaymentsModel.objects.all()
    serializer_class = ProjectPaymentsModelSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return global_response(msg="data deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return global_response(msg="Request data not exist", errors=str(e), status=status.HTTP_400_BAD_REQUEST)
