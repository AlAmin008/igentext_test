# Generated by Django 4.2.4 on 2023-12-26 04:50

from django.db import migrations, models
import ocrapi.models


class Migration(migrations.Migration):

    dependencies = [
        ('ocrapi', '0007_pdffiles_uploaded_time_alter_pdffiles_uploaded_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdffiles',
            name='uploaded_date',
            field=models.DateField(validators=[ocrapi.models.validate_date_format]),
        ),
    ]
