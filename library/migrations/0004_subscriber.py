# Generated by Django 5.1.2 on 2024-10-30 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
