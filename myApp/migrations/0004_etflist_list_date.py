# Generated by Django 4.2.3 on 2023-09-01 05:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0003_etflist_p_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="etflist",
            name="list_date",
            field=models.CharField(max_length=256, null=True, verbose_name="上市时间"),
        ),
    ]