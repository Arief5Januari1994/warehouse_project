# Generated by Django 3.0.7 on 2020-06-24 15:07

from django.db import migrations, models
import django.db.models.deletion
import items.models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20200624_2207'),
        ('items', '0002_remove_item_item_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemHistoryService',
            fields=[
                ('item_history_service_id', models.CharField(default=items.models.ItemHistoryService.increment_service_number, max_length=17, primary_key=True, serialize=False, unique=True)),
                ('service_date', models.DateField()),
                ('detail_service', models.TextField(max_length=800)),
                ('item_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_set', to='items.Item')),
                ('service_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_set', to='employee.Employee')),
            ],
        ),
    ]
