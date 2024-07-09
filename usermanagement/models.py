from django.db import models, transaction
import random
import uuid


class UserAccount(models.Model):
    roles = (
        ("SuperAdmin", "SuperAdmin"),
        ("Admin", "Admin"),
        ("Employee", "Employee"),
        ("Accountant", "Accountant"),
        ("Customer", "Customer"),
    )
    desig = (
        ("ED", "ED"),
        ("GM", "GM"),
        ("AGM", "AGM"),
        ("MO", "MO"),

    )
    id = models.AutoField(primary_key=True, unique=True, null=False)
    uid = models.PositiveIntegerField(unique=True, null=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True)
    password = models.CharField(max_length=256)
    designation = models.CharField(
        max_length=20, choices=desig, blank=True)
    image = models.ImageField(upload_to='photos/users', blank=True)
    role = models.CharField(max_length=50, null=True,
                            blank=True, choices=roles, default="Employee")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    reference_id = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='references')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name_plural = "User Accounts"


    def __str__(self):
        return self.email

    # @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.uid:
            while True:
                uid = random.randint(1000, 99999)
                if not UserAccount.objects.filter(uid=uid).exists():
                    self.uid = uid
                    break
        super().save(*args, **kwargs)
