# Generated by Django 4.1.13 on 2024-05-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='fasttext_vector',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interest',
            name='scibert_vector',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
