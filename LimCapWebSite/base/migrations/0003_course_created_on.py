# Generated by Django 4.2.1 on 2023-08-09 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_paymentstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]