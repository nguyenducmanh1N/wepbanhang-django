# Generated by Django 4.2.5 on 2023-10-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
    ]
