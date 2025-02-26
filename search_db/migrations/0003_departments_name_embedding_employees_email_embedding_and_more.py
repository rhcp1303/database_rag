# Generated by Django 5.1.6 on 2025-02-26 14:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_db', '0002_rename_department_departments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='departments',
            name='name_embedding',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='employees',
            name='email_embedding',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='employees',
            name='name_embedding',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='orders',
            name='customer_name_embedding',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='products',
            name='name_embedding',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None),
        ),
    ]
