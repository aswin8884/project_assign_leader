# Generated by Django 5.0.7 on 2024-08-28 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_add_member_job_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('submission_date', models.DateTimeField(null=True)),
                ('uploaded_date', models.DateTimeField(null=True)),
                ('leader_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.add_leader')),
            ],
        ),
    ]
