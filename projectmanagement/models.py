from django.db import models
from usermanagement.models import UserAccount
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import random
from django.core.exceptions import ValidationError


def validate_non_negative(value):
    if value < 0:
        raise ValidationError(
            '%(value)s is not an allowed value. The value must be non-negative.',
            params={'value': value},
        )


class ProjectsModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    p_id = models.PositiveIntegerField(
        unique=True, null=False)
    # projectDocDet= models.ForeignKey(ProjectDocumentsModel,)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    address = models.CharField(max_length=200, null=True)
    per_share_cost = models.DecimalField(max_digits=12, decimal_places=3,validators=[validate_non_negative])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.p_id:
            while True:
                p_id = random.randint(1000, 99999)
                if not ProjectsModel.objects.filter(p_id=p_id).exists():
                    self.p_id = p_id
                    break
        super().save(*args, **kwargs)


class ProjectDocumentsModel(models.Model):
    file_types = (
        ("jpg", "jpg"),
        ("png", "png"),
        ("pdf", "pdf"),
        ("doc", "doc"),
        ("csv", "csv"),
    )
    id = models.AutoField(primary_key=True, null=False, unique=True)
    project_id = models.ForeignKey(
        ProjectsModel, on_delete=models.CASCADE, related_name='project_documents')
    file_type = models.CharField(max_length=10, choices=file_types, null=True)
    upload_file = models.FileField(upload_to='file/', blank=True, null=True)
    url = models.URLField(null=True)
    pdoc_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.id


class ProjectCustomersModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    project_id = models.ForeignKey(ProjectsModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    total_share = models.IntegerField(validators=[validate_non_negative])
    have_to_pay_amount = models.DecimalField(
        max_digits=10, decimal_places=3, null=True,validators=[validate_non_negative])
    paid = models.DecimalField(max_digits=12, decimal_places=3, null=True,validators=[validate_non_negative])
    # due_amount = models.DecimalField(max_digits=12, decimal_places=3, null=True, validators=[validate_non_negative])  # Added field for due amount
    reference_userId = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, null=True, related_name='customer_registered')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_id.title
    
    # def save(self, *args, **kwargs):  # Modified save method to include due amount calculation
    #     self.have_to_pay_amount = self.project_id.per_share_cost * self.total_share
    #     self.due_amount = self.have_to_pay_amount - self.paid
    #     super().save(*args, **kwargs)


class ProjectCustomerInformationModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    project_customer_id = models.ForeignKey(
        ProjectCustomersModel, on_delete=models.CASCADE)
    customer_image = models.ImageField(
        upload_to='photos/customer', blank=True, null=True)
    customer_name = models.CharField(max_length=30)
    customer_address = models.CharField(max_length=100, null=True, blank=True)
    customer_phone1 = models.CharField(max_length=15, null=True, blank=True)
    customer_phone2 = models.CharField(max_length=15, null=True, blank=True)
    customer_nid_no = models.CharField(max_length=25, null=True, blank=True)
    customer_nid_image = models.ImageField(
        upload_to='photos/customer', blank=True, null=True)
    customer_nominee_name = models.CharField(max_length=30)
    customer_nominee_address = models.CharField(
        max_length=100, null=True, blank=True)
    customer_nominee_nid_image = models.ImageField(
        upload_to='photos/customer', blank=True, null=True)
    customer_nominee_nid_no = models.CharField(
        max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectPaymentsModel(models.Model):
    payment_types = (
        ("booking_money", "booking_money"),
        ("down_payment", "down_payment"),
        ("installment", "installment"),
    )
    id = models.AutoField(primary_key=True, null=False, unique=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    account_log_id = GenericForeignKey(
        'content_type', 'object_id')
    project_id = models.ForeignKey(ProjectsModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='payment_customer')
    reference_user_id = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='payment_reference')
    amount = models.IntegerField(null=True, blank=True,validators=[validate_non_negative])
    payment_type = models.CharField(max_length=30,
                                    choices=payment_types, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
