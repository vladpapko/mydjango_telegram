# Generated by Django 5.0 on 2023-12-23 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_feedback_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='question',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
