# Generated by Django 5.1.3 on 2024-11-12 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryfood', '0003_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=512)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliveryfood.profile')),
            ],
        ),
    ]
