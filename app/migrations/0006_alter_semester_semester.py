# Generated by Django 4.2.5 on 2024-01-21 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_landing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="semester",
            name="semester",
            field=models.CharField(
                blank=True,
                choices=[
                    ("First", "First"),
                    ("Second", "Second"),
                    ("Third", "Third"),
                    ("Final", "Final"),
                ],
                max_length=10,
            ),
        ),
    ]
