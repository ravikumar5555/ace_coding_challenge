# Generated by Django 3.1.1 on 2021-07-18 11:54

from django.db import migrations, models
import django.db.models.deletion
import transaction.models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_number', models.CharField(default=transaction.models.get_transaction_id, max_length=255, unique=True)),
                ('transaction_status', models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('CLOSE', 'CLOSE')], max_length=9)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.branchmaster')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.companyledgermaster')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.departmentmaster')),
            ],
        ),
    ]