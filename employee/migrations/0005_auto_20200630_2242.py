# Generated by Django 3.0.7 on 2020-06-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20200630_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowtransaction',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='division',
            field=models.CharField(choices=[('Manajemen Direksi', 'Manajemen Direksi'), ('', 'Select'), ('Lapangan', 'Lapangan'), ('HSE', 'HSE'), ('Keuangan', 'Keuangan')], max_length=200),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sex',
            field=models.CharField(choices=[('', 'Select'), ('Female', 'Female'), ('Male', 'Male')], default='', max_length=50),
        ),
    ]
