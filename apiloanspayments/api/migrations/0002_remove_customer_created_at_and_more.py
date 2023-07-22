# Generated by Django 4.2.3 on 2023-07-20 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
    ]