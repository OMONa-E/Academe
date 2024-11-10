# Generated by Django 5.1.2 on 2024-11-08 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auditlog_device_info_auditlog_ip_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='changes',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='target_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='target_object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]