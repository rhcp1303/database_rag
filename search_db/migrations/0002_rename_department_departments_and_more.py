# Generated by Django 5.1.6 on 2025-02-26 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search_db', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Department',
            new_name='Departments',
        ),
        migrations.RenameModel(
            old_name='Employee',
            new_name='Employees',
        ),
        migrations.RenameModel(
            old_name='Order',
            new_name='Orders',
        ),
        migrations.RenameModel(
            old_name='Product',
            new_name='Products',
        ),
    ]
