# Generated by Django 4.2.4 on 2023-12-07 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocrapi', '0004_pdffiles_total_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdffiles',
            name='total_size',
            field=models.FloatField(null=True),
        ),
    ]