# Generated by Django 4.2.8 on 2024-05-22 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0005_remove_depositproduct_dcls_end_day_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositproduct',
            name='dcls_month',
        ),
        migrations.AlterField(
            model_name='depositoption',
            name='rsrv_type',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='depositoption',
            name='rsrv_type_nm',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='optionlist',
            name='rsrv_type',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='optionlist',
            name='rsrv_type_nm',
            field=models.CharField(max_length=20, null=True),
        ),
    ]