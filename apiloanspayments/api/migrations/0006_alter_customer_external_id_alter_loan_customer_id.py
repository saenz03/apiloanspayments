# Generated by Django 4.2.3 on 2023-07-21 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_loan_contract_version_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='external_id',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customer', to_field='external_id'),
        ),
    ]
