# Generated by Django 4.2.3 on 2023-08-24 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_loan_dateofdisposal_alter_loan_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Paid', 'Paid')], max_length=10),
        ),
    ]
