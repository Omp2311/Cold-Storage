# Generated by Django 5.1.6 on 2025-03-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0011_alter_store_options_remove_store_chamber_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='chamber_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
