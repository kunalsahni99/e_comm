# Generated by Django 5.2 on 2025-05-02 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orderID',
            new_name='order_id',
        ),
    ]
