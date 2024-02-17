# Generated by Django 4.2.7 on 2023-11-18 01:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("newslist", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newslistdata",
            name="pub_date",
        ),
        migrations.AddField(
            model_name="newslistdata",
            name="keyword",
            field=models.CharField(default="", max_length=10),
            preserve_default=False,
        ),
    ]
