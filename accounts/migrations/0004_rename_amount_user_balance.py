# Generated by Django 5.0.1 on 2024-01-20 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='amount',
            new_name='balance',
        ),
    ]
