# Generated by Django 3.2.18 on 2023-05-09 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lb_models", "0002_auto_20230508_1331"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monitor",
            name="args",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
