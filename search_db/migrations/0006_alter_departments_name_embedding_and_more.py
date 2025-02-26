# Generated by Django 5.1.6 on 2025-02-26 17:38

import pgvector.django.vector
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search_db', '0005_alter_departments_name_embedding_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='name_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=768, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='email_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=768, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='name_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=768, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='customer_name_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=768, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='name_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=768, null=True),
        ),
    ]
