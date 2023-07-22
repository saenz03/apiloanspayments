# Generated by Django 4.2.3 on 2023-07-21 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_loan_customer_id_alter_customer_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='external_id',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='customer_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.customer', to_field='external_id'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='loan_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.loan', to_field='external_id'),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='payment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.payment'),
        ),
        migrations.AlterField(
            model_name='paymentdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
