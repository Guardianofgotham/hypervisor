# Generated by Django 5.1.4 on 2024-12-08 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
