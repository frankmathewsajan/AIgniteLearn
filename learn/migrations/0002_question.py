# Generated by Django 5.1.3 on 2024-11-09 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500)),
                ('options', models.JSONField()),
                ('correct_option', models.CharField(max_length=100)),
            ],
        ),
    ]
