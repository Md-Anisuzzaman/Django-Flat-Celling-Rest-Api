# Generated by Django 5.0.6 on 2024-06-20 18:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanagement', '0003_alter_projectcustomerinformationmodel_customer_nid_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdocumentsmodel',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_documents', to='projectmanagement.projectsmodel'),
        ),
    ]
