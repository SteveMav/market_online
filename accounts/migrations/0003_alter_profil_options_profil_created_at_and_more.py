# Generated by Django 5.1 on 2025-05-12 18:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profil_phone_number_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profil',
            options={'ordering': ['-created_at'], 'verbose_name': 'Profil', 'verbose_name_plural': 'Profils'},
        ),
        migrations.AddField(
            model_name='profil',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date de création'),
        ),
        migrations.AddField(
            model_name='profil',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Dernière mise à jour'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='bio',
            field=models.TextField(blank=True, help_text='Une brève description de vous-même', null=True, verbose_name='Biographie'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='commune',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Commune'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Masculin'), ('F', 'Féminin'), ('O', 'Autre')], max_length=1, null=True, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='interests',
            field=models.TextField(blank=True, help_text="Vos centres d'intérêt, séparés par des virgules", null=True, verbose_name="Centres d'intérêt"),
        ),
        migrations.AlterField(
            model_name='profil',
            name='is_seller',
            field=models.BooleanField(default=False, help_text="Indique si l'utilisateur peut vendre des produits", verbose_name='Vendeur'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='phone_number',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/%Y/%m/', verbose_name='Photo de profil'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil', to=settings.AUTH_USER_MODEL),
        ),
    ]
