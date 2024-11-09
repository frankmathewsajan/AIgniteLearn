# Generated by Django 5.1.3 on 2024-11-09 06:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('learning_style', models.CharField(blank=True, max_length=50)),
                ('education_level', models.CharField(blank=True, max_length=50)),
                ('interests', models.JSONField(blank=True, default=list)),
                ('goals', models.JSONField(blank=True, default=list)),
                ('is_setup', models.BooleanField(default=False)),
                ('avatar', models.ImageField(default='profile_images/default.png', upload_to='profile_images')),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]