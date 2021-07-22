# Generated by Django 3.1.1 on 2021-07-20 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_inventoryitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineitem',
            old_name='item_id',
            new_name='line_item_id',
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='line_item_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='transaction.lineitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lineitem',
            name='transaction_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='transaction.transaction'),
            preserve_default=False,
        ),
    ]
