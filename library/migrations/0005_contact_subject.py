# Generated by Django 5.1.2 on 2024-10-30 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
