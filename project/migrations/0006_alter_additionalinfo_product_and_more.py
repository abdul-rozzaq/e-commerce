# Generated by Django 5.1.2 on 2024-10-31 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalinfo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='infos', to='project.product'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project.product'),
        ),
    ]