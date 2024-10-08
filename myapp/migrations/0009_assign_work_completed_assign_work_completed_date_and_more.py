# Generated by Django 5.0.7 on 2024-08-29 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_rename_status_add_member_assigned_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign_work',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assign_work',
            name='completed_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='assign_work',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
