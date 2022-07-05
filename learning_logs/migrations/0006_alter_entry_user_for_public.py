# Generated by Django 4.0.5 on 2022-07-05 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning_logs', '0005_entry_user_for_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='user_for_public',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
