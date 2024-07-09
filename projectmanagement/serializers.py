from rest_framework import serializers
from .models import (
    ProjectsModel,
    ProjectDocumentsModel,
    ProjectCustomersModel,
    ProjectCustomerInformationModel,
    ProjectPaymentsModel,
)
from usermanagement.serializers import UserInfoSerializer


class ProjectDocumentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocumentsModel
        fields = '__all__'


class ProjectsModelSerializer(serializers.ModelSerializer):
    project_documents = ProjectDocumentsModelSerializer(
        many=True, read_only=True)

    class Meta:
        model = ProjectsModel
        read_only_fields = ['p_id']
        # fields = '__all__'
        fields = ['id', 'p_id', 'title', 'description', 'address',
                  'per_share_cost', 'created_at', 'updated_at', 'project_documents']


class ProjectCustomersModelSerializer(serializers.ModelSerializer):
    project_id = ProjectsModelSerializer(read_only=True)
    user_id = UserInfoSerializer(read_only=True)
    reference_userId = UserInfoSerializer(read_only=True)

    class Meta:
        model = ProjectCustomersModel
        fields = '__all__'


class ProjectCustomerInformationModelSerializer(serializers.ModelSerializer):
    project_customer_id = ProjectCustomersModelSerializer(read_only=True)

    class Meta:
        model = ProjectCustomerInformationModel
        fields = '__all__'


class ProjectPaymentsModelSerializer(serializers.ModelSerializer):
    # project_id = ProjectsModelSerializer(read_only=True)
    # user_id = UserInfoSerializer(read_only=True)
    # reference_user_id = UserInfoSerializer(read_only=True)
    project = ProjectsModelSerializer(read_only=True, source='project_id')
    user = UserInfoSerializer(read_only=True, source='user_id')
    reference_user_by_registerd = UserInfoSerializer(
        read_only=True, source='reference_user_id')

    class Meta:
        model = ProjectPaymentsModel
        fields = '__all__'
        # fields = [
        #     'id',
        #     'amount',
        #     'payment_type',
        #     'created_at',
        #     'updated_at',
        #     'project',
        #     'user',
        #     'reference_user_by_registerd',
        #     'object_id',
        #     'content_type'
        # ]

# single project er sob customer info
# projects/projectid/coustomers
# ekta project er under e ki ki coustomer ache
#project details with customer
#project e koto tk deyar chilo koto tk deya ache  

# nicherta single project er single customer info
# projects/projectid/coustomer/coustomerId

