# Generated by Django 4.2.3 on 2023-09-01 05:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0002_etflist"),
    ]

    operations = [
        migrations.AddField(
            model_name="etflist",
            name="p_value",
            field=models.CharField(max_length=256, null=True, verbose_name="面值"),
        ),
    ]
