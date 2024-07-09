from rest_framework import serializers
from .models import ProjectsModel, ProjectDocumentsModel, ProjectCustomersModel, ProjectPaymentsModel,ProjectCustomerInformationModel
from usermanagement.serializers import UserInfoSerializer

class ProjectDocumentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocumentsModel
        fields = '__all__'

class ProjectsModelSerializer(serializers.ModelSerializer):
    project_documents = ProjectDocumentsModelSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectsModel
        read_only_fields = ['p_id']
        fields = ['id', 'p_id', 'title', 'description', 'address', 'per_share_cost', 'created_at', 'updated_at', 'project_documents']

class ProjectPaymentsModelSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True, source='user_id')
    reference_user_by_registerd = UserInfoSerializer(read_only=True, source='reference_user_id')

    class Meta:
        model = ProjectPaymentsModel
        fields = ['id', 'amount', 'payment_type', 'created_at', 'updated_at', 'user', 'reference_user_by_registerd']

class ProjectCustomersModelSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True, source='user_id')
    reference_user = UserInfoSerializer(read_only=True, source='reference_userId')
    payments = ProjectPaymentsModelSerializer(many=True, read_only=True, source='projectpaymentsmodel_set')
    due_amount = serializers.SerializerMethodField()

    class Meta:
        model = ProjectCustomersModel
        fields = ['id', 'user', 'total_share', 'have_to_pay_amount', 'paid', 'due_amount', 'reference_user', 'created_at', 'updated_at', 'payments']

    def get_due_amount(self, obj):
        return obj.have_to_pay_amount - obj.paid if obj.have_to_pay_amount and obj.paid else None

class ProjectCustomerInformationModelSerializer(serializers.ModelSerializer):
    project_customer_id = ProjectCustomersModelSerializer(read_only=True)

    class Meta:
        model = ProjectCustomerInformationModel
        fields = '__all__'

class ProjectDetailSerializer(serializers.ModelSerializer):
    project_documents = ProjectDocumentsModelSerializer(many=True, read_only=True)
    customers = ProjectCustomersModelSerializer(many=True, read_only=True, source='projectcustomersmodel_set')

    class Meta:
        model = ProjectsModel
        fields = ['id', 'p_id', 'title', 'description', 'address', 'per_share_cost', 'created_at', 'updated_at', 'project_documents', 'customers']


# class DetailedCustomerSerializer(serializers.ModelSerializer):
#     project = ProjectsModelSerializer(read_only=True, source='project_id')
#     payments = ProjectPaymentsModelSerializer(many=True, read_only=True, source='projectpaymentsmodel_set')
#     user = UserInfoSerializer(read_only=True, source='user_id')
#     reference_user = UserInfoSerializer(read_only=True, source='reference_userId')
#     due_amount = serializers.SerializerMethodField()
#     # due_amount = serializers.DecimalField(max_digits=12, decimal_places=3, read_only=True)  # Added field for due amount

#     class Meta:
#         model = ProjectCustomersModel
#         fields = ['id', 'user', 'total_share', 'have_to_pay_amount', 'paid', 'due_amount', 'reference_user', 'created_at', 'updated_at', 'project', 'payments']

#     def get_due_amount(self, obj):
#         return obj.have_to_pay_amount - obj.paid if obj.have_to_pay_amount and obj.paid else None
    
    
    
class SingleCustomerDetailsSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True, source='user_id')
    reference_user = UserInfoSerializer(read_only=True, source='reference_userId')
    payments = ProjectPaymentsModelSerializer(many=True, read_only=True, source='projectpaymentsmodel_set')
    due_amount = serializers.SerializerMethodField()

    class Meta:
        model = ProjectCustomersModel
        fields = ['id', 'user', 'total_share', 'have_to_pay_amount', 'paid', 'due_amount', 'reference_user', 'created_at', 'updated_at', 'payments']

    def get_due_amount(self, obj):
        return obj.have_to_pay_amount - obj.paid if obj.have_to_pay_amount and obj.paid else None