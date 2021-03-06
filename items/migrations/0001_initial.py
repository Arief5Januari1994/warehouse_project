# Generated by Django 3.0.7 on 2020-06-16 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('item_code', models.CharField(max_length=8)),
                ('item_merk', models.CharField(max_length=100)),
                ('item_picture', models.ImageField(upload_to='upload')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Category')),
            ],
        ),
    ]
