# Generated by Django 2.1.5 on 2019-02-10 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20190210_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(db_index=True, max_length=150, unique=True),
        ),
    ]
