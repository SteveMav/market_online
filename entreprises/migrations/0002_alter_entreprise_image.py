# Generated by Django 5.1 on 2025-03-26 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entreprises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprise',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images_entreprises/'),
        ),
    ]
